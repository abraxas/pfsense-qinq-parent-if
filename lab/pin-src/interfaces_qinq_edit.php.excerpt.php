<?php
/* Pin excerpt pfsense/pfsense 9363ac5b8651a1c7a333180425ce7719070f95f9. Do not edit by hand. */

function get_vlan_tag_types() {
	return [
		'ctag' => 'C-Tag (0x8100)',
		'stag' => 'S-Tag (0x88A8)'
	];
}

function qinq_edit_save() {
	global $id, $this_qinq_config, $input_errors, $qinqentry, $nmembers, $posted_members;
	$input_errors = array();
	$posted_members = '';
	if (!array_key_exists($_POST['tag_type'], get_vlan_tag_types())) {
		$input_errors[] = gettext("The selected VLAN Tag Type is invalid.");
	}

	if (empty($_POST['tag'])) {
		$input_errors[] = gettext("First level tag cannot be empty.");
	}
	if ($this_qinq_config && $this_qinq_config['tag'] != $_POST['tag']) {
		$input_errors[] = gettext("Modifying the first level tag of an existing entry is not allowed.");
	}
	if ($this_qinq_config && $this_qinq_config['if'] != $_POST['if']) {
		$input_errors[] = gettext("Modifying the interface of an existing entry is not allowed.");
	}
	if (!isset($id)) {
		foreach (config_get_path('qinqs/qinqentry', []) as $qinqentry) {
			if ($qinqentry['tag'] == $_POST['tag'] && $qinqentry['if'] == $_POST['if']) {
				$input_errors[] = gettext("QinQ level already exists for this interface, edit it!");
			}
		}
		foreach (config_get_path('vlans/vlan', []) as $vlan) {
			if ($vlan['tag'] == $_POST['tag'] && $vlan['if'] == $_POST['if']) {
				$input_errors[] = gettext("A normal VLAN exists with this tag please remove it to use this tag for QinQ first level.");
			}
		}
	}

	$qinqentry = array();
	$qinqentry['if'] = $_POST['if'];
	$qinqentry['tag_type'] = $_POST['tag_type'];
	$qinqentry['tag'] = $_POST['tag'];

	if ($_POST['autogroup'] == "yes") {
		$qinqentry['autogroup'] = true;
	}

	$tag_min = 1;
	$tag_max = 4094;
	$tag_format_error = false;
	$members = "";

	// Read the POSTed member array into a space separated list translating any ranges
	// into their included values
	$membercounter = 0;
	$membername = "member{$membercounter}";
	$valid_members = array();

	while (isset($_POST[$membername])) {
		if (is_intrange($_POST[$membername], $tag_min, $tag_max)) {
			$sep = (strpos($_POST[$membername], ":") === false) ? "-" : ":";
			$member = explode($sep, $_POST[$membername]);
			for ($i = intval($member[0]); $i <= intval($member[1]); $i++) {
				$valid_members[] = $i;
			}
		} elseif (is_numericint($_POST[$membername]) && ($_POST[$membername] >= $tag_min) && ($_POST[$membername] <= $tag_max)) {
			$valid_members[] = intval($_POST[$membername]);
		} elseif ($_POST[$membername] != "") {
			$tag_format_error = true;
		} // else ignore empty rows

		// Remember the POSTed values so they can be redisplayed if there were errors.
		$posted_members .= ($membercounter == 0 ? '':' ') . $_POST[$membername];

		$membercounter++;
		$membername = "member{$membercounter}";
	}

	if ($tag_format_error) {
		$input_errors[] = sprintf(gettext('Tags can contain only numbers or a range  (in format #-#) from %1$s to %2$s.'), $tag_min, $tag_max);
	}

	// Just use the unique valid members. There could have been overlap in the ranges or repeat of numbers entered.
	$members = implode(" ", array_unique($valid_members));

	if ($members == "") {
		$input_errors[] = gettext("At least one tag must be entered.");
	}

	$nmembers = explode(" ", $members);
	if ($this_qinq_config) {
		$omembers = explode(" ", $this_qinq_config['members']);
		$delmembers = array_diff($omembers, $nmembers);
		foreach ($delmembers as $tag) {
			if (qinq_inuse($this_qinq_config, $tag)) {
				$input_errors[] = gettext("This QinQ tag cannot be deleted because it is still being used as an interface.");
				break;
			}
		}
	}

	if (!$input_errors) {
		$qinqentry['members'] = $members;
		$qinqentry['descr'] = $_POST['descr'];
		$qinqentry['vlanif'] = vlan_interface($_POST);
		$nmembers = explode(" ", $members);

		if ($this_qinq_config) {
			$omembers = explode(" ", $this_qinq_config['members']);
			$delmembers = array_diff($omembers, $nmembers);
			$addmembers = array_diff($nmembers, $omembers);

			if ((count($delmembers) > 0) || (count($addmembers) > 0)) {
				$parent = $qinqentry['vlanif'];
				foreach ($delmembers as $tag) {
					exec("/sbin/ifconfig {$parent}.{$tag} destroy");
				}

				foreach ($addmembers as $member) {
					$qinq = array();
					$qinq['if'] = $qinqentry['vlanif'];
					$qinq['tag'] = $member;
					interface_qinq2_configure($qinq);
				}
			}
			config_set_path("qinqs/qinqentry/{$id}", $qinqentry);

			interface_vlan_set_tag_type($qinqentry['vlanif'], $qinqentry['tag_type']);
		} else {
			interface_qinq_configure($qinqentry);
			config_set_path('qinqs/qinqentry/', $qinqentry);
		}

		write_config("QinQ interface added");
	}
}
