package require uri
package require fcgi
package require sqlite3
package require rest

#https://stackoverflow.com/questions/31839282/http-get-request-tcl
proc geturl_followRedirects {url args} {
	array set URI [::uri::split $url]
	for {set i 0} {$i < 5} {incr i} {
		set token [::http::geturl $url {*}$args]
		if {![string match {30[1237]} [::http::ncode $token]]} {return $token}
		set location [lmap {k v} [set ${token}(meta)] {
			if {[string match -nocase location $k]} {set v} continue
		}]
		if {$location eq {}} {
			return $token
		}
		array set uri [::uri::split $location]
		if {$uri(host) eq {}} {set uri(host) $URI(host)}
		# problem w/ relative versus absolute paths
		set url [::uri::join {*}[array get uri]]
	}
}

set curdir [file dirname [info script]]

#source [file join $curdir "TemplaTcl.tcl"]

fcgi Init
set sock [fcgi OpenSocket :8000]
set req [fcgi InitRequest $sock 0]

while {1} {
	fcgi Accept_r $req
	#get the requested page
	set pd [fcgi GetParam $req]
	set request_str [dict get $pd REQUEST_URI]
	
	set C "Status: 200 OK\n"
	#generate the page
	append C "Content-Type: "
	append C "text/html"
	append C "\r\n\r\n"
	
	set query_params [rest::parameters $request_str]
	
	if [dict exists $query_params action] {
		if {[dict get $query_params action] eq "check"} {
			set allowed [::http::data [geturl_followRedirects "http://localhost:8062/check"]]
			if {[lindex $allowed 0] > 0} {
				puts $allowed
				set auth_user_name [lindex $allowed 1]
				append C "Hello, $auth_user_name."
			} elseif {[lindex $allowed 0] == 0} {
				append C "No face detected..."
			} elseif {[lindex $allowed 0] == -1} {
				append C "Face not recognized."
			} else {
				append C "Bad output from Face API server!"
			}
		} elseif {[dict get $query_params action] eq "verify"} {
			set theCode [format "%06d" [expr {int(1000000 * rand())}]]
			append C "Please enter the code $theCode on the mobile app."
			geturl_followRedirects "http://localhost:8061/$theCode"
		}
	} else {
		append C "null home page"
	}
	
	#output the page
	fcgi PutStr $req stdout $C
	fcgi SetExitStatus $req stdout 0
	fcgi Finish_r $req
}