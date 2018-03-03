package require fcgi
package require sqlite3
package require rest

set curdir [file dirname [info script]]

source [file join $curdir "TemplaTcl.tcl"]

fcgi Init
set sock [fcgi OpenSocket :8000]
set req [fcgi InitRequest $sock 0]
sqlite3 sitedb [file join $curdir "sites.db"]

set templates [dict create]

while {1} {
	fcgi Accept_r $req
	#get the requested page
	set pd [fcgi GetParam $req]
	set request_str [dict get $pd REQUEST_URI]
	if {$request_str eq "/"} {
		set request_str "/cgi-bin/getpage.cgi?p=1"
	}
	set query_params [rest::parameters $request_str]
	if [dict exists $query_params p] {
		set id [dict get $query_params p]
		#generate the page
		set C "Status: 200 OK\n"
		set page [sitedb eval {SELECT Name,ID,Content,Template,ContentType,Parent FROM Pages WHERE ID=$id ORDER BY Version DESC;}]
		if {$page ne ""} {
			append C "Content-Type: "
			append C [lindex $page 4]
			append C "\r\n\r\n"
			set TemplateID [lindex $page 3]
			if $TemplateID {
				if {![dict exists $templates $TemplateID]} {
					set template "TEMPLATE_OBJ_$TemplateID"
					TemplaTcl::create $template
					dict append templates $TemplateID $template
					$template parse [lindex [sitedb eval {SELECT TemplateText FROM Templates WHERE ID=$TemplateID;}] 0]
				} else {
					set template [dict get $templates $TemplateID]
				}
				$template setVar NAME [lindex $page 0]
				$template setVar ID [lindex $page 1]
				$template setVar CONTENT [lindex $page 2]
				$template setVar TEMPLATE [lindex $page 3]
				$template setVar CONTENTTYPE [lindex $page 4]
				$template setVar PARENT [lindex $page 5]
				append C [$template render]
			} else {
				append C [lindex $page 2]
			}
		} else {
			set C "Status: 200 OK\n"
			append C "Page not found. Query: "
			append C [dict get $pd REQUEST_URI]
		}
	} else {
		set C "Status: 200 OK\n"
		append C "Invalid query. Query: "
		append C [dict get $pd REQUEST_URI]
	}
	
	#output the page
	fcgi PutStr $req stdout $C
	fcgi SetExitStatus $req stdout 0
	fcgi Finish_r $req
}
