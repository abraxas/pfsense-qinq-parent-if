<?php
/* pfSense CE 2.9.0-DEVELOPMENT QinQ parent-if gadget. Pin 9363ac5. */

require __DIR__ . '/stubs.php';
require __DIR__ . '/pin-src/globals.inc.excerpt.php';
require __DIR__ . '/pin-src/util.inc.excerpt.php';
require __DIR__ . '/pin-src/interfaces.inc.excerpt.php';
require __DIR__ . '/pin-src/interfaces_vlan_edit.php.excerpt.php';
require __DIR__ . '/pin-src/interfaces_qinq_edit.php.excerpt.php';

function lab_fail(string $reason): void {
	echo json_encode(array('ok' => false, 'error' => $reason), JSON_UNESCAPED_SLASHES) . "\n";
	exit(1);
}

function lab_members_payload(array $payload, string $key): array {
	$raw = $payload[$key] ?? array();
	if (!is_array($raw)) {
		lab_fail("bad-{$key}");
	}
	$out = array();
	foreach ($raw as $item) {
		$out[] = strval($item);
	}
	return $out;
}

function lab_qinq2_meta(?string $vlanif, array $members): array {
	$rows = array();
	if ($vlanif === null) {
		return $rows;
	}
	foreach ($members as $member) {
		$name = "{$vlanif}.{$member}";
		$rows[] = array(
			'name_len' => strlen($name),
			'over_namesize' => strlen($name) > IF_NAMESIZE,
		);
	}
	return $rows;
}

function lab_log_text(): string {
	$parts = array();
	foreach ($GLOBALS['lab_logs'] as $row) {
		$parts[] = $row['message'];
	}
	return implode("\n", $parts);
}

$mode = $argv[1] ?? '';
$raw = $argv[2] ?? '{}';
$payload = json_decode($raw, true);
if (!is_array($payload)) {
	lab_fail('bad-json');
}

$post_if = strval($payload['if'] ?? '');
$post_tag = strval($payload['tag'] ?? '1');
$post_type = strval($payload['tag_type'] ?? 'stag');
$members = lab_members_payload($payload, 'members');
$existing_members = lab_members_payload($payload, 'existing_members');

$_POST = array(
	'if' => $post_if,
	'tag' => $post_tag,
	'tag_type' => $post_type,
	'descr' => strval($payload['descr'] ?? ''),
	'autogroup' => '',
	'save' => 'yes',
);
foreach ($members as $idx => $member) {
	$_POST['member' . $idx] = $member;
}

$id = null;
$this_qinq_config = null;
$input_errors = array();
$qinqentry = array();
$nmembers = array();
$posted_members = '';

$vlan_rejected = false;
$create_invalid_if = false;

if ($mode === 'vlan-edit') {
	vlan_edit_reject_missing_parent($post_if, $input_errors);
	foreach ($input_errors as $err) {
		if ($err === 'Interface supplied as parent is invalid') {
			$vlan_rejected = true;
		}
	}
} elseif ($mode === 'qinq-create' || $mode === 'qinq-edit') {
	if ($mode === 'qinq-edit') {
		$id = 0;
		$this_qinq_config = array(
			'if' => $post_if,
			'tag' => $post_tag,
			'tag_type' => $post_type,
			'members' => implode(' ', $existing_members),
			'descr' => '',
		);
		$this_qinq_config['vlanif'] = vlan_interface($this_qinq_config);
	}
	qinq_edit_save();
	$create_invalid_if = str_contains(lab_log_text(), 'called with invalid if.');
} else {
	lab_fail('bad-mode');
}

$vlanif = is_array($qinqentry) && isset($qinqentry['vlanif'])
	? $qinqentry['vlanif']
	: vlan_interface($_POST);

$result = array(
	'ok' => true,
	'mode' => $mode,
	'errors' => $input_errors,
	'write_config' => $GLOBALS['lab_write_config'],
	'write_desc' => $GLOBALS['lab_write_desc'],
	'vlan_rejected' => $vlan_rejected,
	'create_invalid_if' => $create_invalid_if,
	'vlanif' => $vlanif,
	'vlanif_len' => is_string($vlanif) ? strlen($vlanif) : 0,
	'if_namesize' => IF_NAMESIZE,
	'qinq2' => lab_qinq2_meta(is_string($vlanif) ? $vlanif : null, $members),
	'stored' => $GLOBALS['lab_config'],
	'mwexec_count' => count($GLOBALS['lab_mwexec']),
	'vlan_configure_count' => count($GLOBALS['lab_vlan_configure']),
	'logs' => array_map(
		static function ($row) {
			return $row['message'];
		},
		$GLOBALS['lab_logs']
	),
);

echo json_encode($result, JSON_UNESCAPED_SLASHES) . "\n";
