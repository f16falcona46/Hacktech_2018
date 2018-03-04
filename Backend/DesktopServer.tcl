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

source [file join $curdir "TemplaTcl.tcl"]
TemplaTcl::create checkTemplate
checkTemplate parseFile [file join $curdir "check.htmlt"]
TemplaTcl::create verify_step1Template
verify_step1Template parseFile [file join $curdir "verify_step1.htmlt"]
TemplaTcl::create verify_step2Template
verify_step2Template parseFile [file join $curdir "verify_step2.htmlt"]
TemplaTcl::create verify_step3Template
verify_step3Template parseFile [file join $curdir "verify_step3.htmlt"]

sqlite3 verifyDb [file join $curdir "verification.db"]

fcgi Init
set sock [fcgi OpenSocket :8000]
set req [fcgi InitRequest $sock 0]

while {1} {
	fcgi Accept_r $req
	#get the requested page
	set pd [fcgi GetParam $req]
	set request_str [dict get $pd "REQUEST_URI"]
	
	set C "Status: 200 OK\n"
	#generate the page
	append C "Content-Type: "
	append C "text/html"
	append C "\r\n\r\n"
	
	set query_params [rest::parameters $request_str]
	
	if [dict exists $query_params "action"] {
		if {[dict get $query_params "action"] eq "check"} {
			set allowed [::http::data [geturl_followRedirects "http://localhost:8062/check"]]
			checkTemplate setVar UNLOCKED [expr {[lindex $allowed 0] == 1}]
			if {[lindex $allowed 0] > 0} {
				set auth_user_name [lindex $allowed 1]
				checkTemplate setVar FACESTATUS "Hello, $auth_user_name."
			} elseif {[lindex $allowed 0] == 0} {
				checkTemplate setVar FACESTATUS "No face detected..."
			} elseif {[lindex $allowed 0] == -1} {
				checkTemplate setVar FACESTATUS "Face not recognized."
			} else {
				checkTemplate setVar FACESTATUS "Bad output from Face API server!"
			}
			append C [checkTemplate render]
		} elseif {[dict get $query_params "action"] eq "verify_step1"} {
			append C [verify_step1Template render]
		} elseif {[dict get $query_params "action"] eq "verify_step2"} {
			if [dict exists $query_params "phone_number"] {
				set phoneNumber [dict get $query_params "phone_number"]
				set theCode [format "%06d" [expr {int(1000000 * rand())}]]
				geturl_followRedirects "http://localhost:8061/$theCode,$phoneNumber"
				verifyDb eval {INSERT INTO VerificationRequests (PhoneNumber, VerificationCode) VALUES($phoneNumber, $theCode);}
				append C [verify_step2Template render]
			} else {
				append C "No phone number was entered."
			}
		} elseif {[dict get $query_params "action"] eq "verify_step3"} {
			if [dict exists $query_params "verification_code"] {
				set verificationCode [dict get $query_params "verification_code"]
				set verificationResult [verifyDb eval {SELECT PhoneNumber FROM VerificationRequests WHERE VerificationCode = $verificationCode ORDER BY Id DESC}]
				if {$verificationResult ne ""} {
					set phoneNumber [lindex $verificationResult 0]
					verify_step3Template setVar SUCCESS "Success! Your phone (phone number $phoneNumber) is now verified."
				} else {
					verify_step3Template setVar SUCCESS "Incorrect verification code, please try again."
				}
				append C [verify_step3Template render]
			} else {
				append C "No verification code was entered."
			}
		}
	} else {
		append C "null home page"
	}
	
	#output the page
	fcgi PutStr $req stdout $C
	fcgi SetExitStatus $req stdout 0
	fcgi Finish_r $req
}