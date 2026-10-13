<?php
/* Pin excerpt pfsense/pfsense 9363ac5b8651a1c7a333180425ce7719070f95f9. Do not edit by hand. */

function vlan_edit_reject_missing_parent($post_if, array &$input_errors) {
	$_POST = array('if' => $post_if);
	if (!does_interface_exist($_POST['if'])) {
		$input_errors[] = gettext("Interface supplied as parent is invalid");
	}
}
