<?php
/* Lab stubs for pin excerpts. does_interface_exist is false for the stored parent. */

$GLOBALS['lab_live_ifs'] = array('em0');
$GLOBALS['lab_config'] = array();
$GLOBALS['lab_logs'] = array();
$GLOBALS['lab_write_config'] = false;
$GLOBALS['lab_write_desc'] = '';
$GLOBALS['lab_mwexec'] = array();
$GLOBALS['lab_vlan_configure'] = array();
$GLOBALS['lab_bring_up'] = array();

function gettext($text) {
	return $text;
}

function localize_text($text, ...$args) {
	if (count($args) === 0) {
		return $text;
	}
	return vsprintf($text, $args);
}

function logger($priority, $message) {
	$GLOBALS['lab_logs'][] = array(
		'priority' => $priority,
		'message' => $message,
	);
	fwrite(STDERR, "logger:{$priority}:{$message}\n");
}

function does_interface_exist($interface, $flush = false) {
	if (!$interface) {
		return false;
	}
	return in_array($interface, $GLOBALS['lab_live_ifs'], true);
}

function write_config($desc = "Unknown", $backup = true, $write_config_only = false) {
	$GLOBALS['lab_write_config'] = true;
	$GLOBALS['lab_write_desc'] = $desc;
}

function config_get_path(string $path, $default = null) {
	if (array_key_exists($path, $GLOBALS['lab_config'])) {
		return $GLOBALS['lab_config'][$path];
	}
	return $default;
}

function config_set_path(string $path, $value, $default = null) {
	$GLOBALS['lab_config'][$path] = $value;
	return $value;
}

function mwexec($command, $nologentry = false) {
	$GLOBALS['lab_mwexec'][] = $command;
	exec($command);
	return 0;
}

function interface_vlan_configure(&$vlan, $flush = true, $skip_parent_mtu = false) {
	$GLOBALS['lab_vlan_configure'][] = $vlan['if'] ?? '';
	if (!empty($vlan['vlanif'])) {
		return $vlan['vlanif'];
	}
	return vlan_interface($vlan);
}

function interfaces_bring_up($interface) {
	$GLOBALS['lab_bring_up'][] = $interface;
}

function get_interface_arr($flush = false) {
	return $GLOBALS['lab_live_ifs'];
}

function interface_is_vlan($if = NULL) {
	return NULL;
}

function qinq_inuse($qinq = NULL, $inqtag = NULL) {
	return false;
}

function interface_vlan_set_tag_type($vlanif, $tag_type) {
	return;
}
