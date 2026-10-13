<?php
/* Pin excerpt pfsense/pfsense 9363ac5b8651a1c7a333180425ce7719070f95f9. Do not edit by hand. */

function vlan_valid_tag($tag = NULL) {

	if ($tag == NULL || empty($tag) ||
	    !is_numericint($tag) || intval($tag) < 1 || intval($tag) > 4094) {
		return (false);
	}
	return (true);
}
function qinq_interface($qinq = NULL, $inqtag = NULL) {

	if ($qinq == NULL || $inqtag == NULL || !is_array($qinq) ||
	    !isset($qinq['if']) || !isset($qinq['tag']) ||
	    !vlan_valid_tag($qinq['tag']) || !vlan_valid_tag($inqtag)) {
		return (NULL);
	}
	return ("{$qinq['if']}.{$qinq['tag']}.{$inqtag}");
}
function vlan_interface($vlan = NULL) {
	if ($vlan == NULL || !is_array($vlan) || !isset($vlan['if']) ||
	    !isset($vlan['tag']) || !vlan_valid_tag($vlan['tag'])) {
		return (NULL);
	}
	return ("{$vlan['if']}.{$vlan['tag']}");
}
function interface_qinq_configure(&$qinq, $flush = true) {
	global $g;

	if (!is_array($qinq)) {
		logger(LOG_DEBUG, localize_text("%s called with wrong options. Problems with config!", "interface_qinq_configure:"));
		return;
	}

	$qinqif = $qinq['if'];
	if (empty($qinqif)) {
		logger(LOG_DEBUG, localize_text("%s called with if undefined.", "interface_qinq_configure"));
		return;
	}

	if (!does_interface_exist($qinqif)) {
		logger(LOG_DEBUG, localize_text("%s called with invalid if.", "interface_qinq_configure"));
		return;
	}

	$vlanif = interface_vlan_configure($qinq);
	if ($vlanif == NULL || $vlanif != $qinq['vlanif']) {
		logger(LOG_ERR, localize_text("%s cannot create VLAN interface", 'interface_qinq_configure'));
		return;
	}

	/* make sure the parent is up */
	interfaces_bring_up($qinqif);

	/* invalidate interface cache */
	if ($flush) {
		get_interface_arr(true);
	}

	if (interface_is_vlan($qinqif) == NULL) {
		mwexec("/sbin/ifconfig {$qinqif} promisc\n");
	}

	if (!empty($qinq['members'])) {
		$members = explode(" ", $qinq['members']);
		foreach ($members as $qtag) {
			$qinq2 = array();
			$qinq2['tag'] = $qtag;
			$qinq2['if'] = $vlanif;
			interface_qinq2_configure($qinq2);
			unset($qinq2);
		}
	}

	interfaces_bring_up($qinqif);
	if (!empty($qinq['members'])) {
		$members = explode(" ", $qinq['members']);
		foreach ($members as $qtag) {
			interfaces_bring_up(qinq_interface($qinq, $qtag));
		}
	}

	return $vlanif;
}
function interface_qinq2_configure(&$qinq) {
	if (!is_array($qinq)) {
		logger(LOG_DEBUG, localize_text("%s called with wrong options. Problems with config!", "interface_qinq2_configure"));
		return;
	}

	$if = $qinq['if'];
	if (empty($if)) {
		logger(LOG_DEBUG, localize_text("%s called with if undefined.", "interface_qinq2_configure"));
		return;
	}
	$tag = $qinq['tag'];
	$vlanif = "{$if}.{$tag}";
	$ngif = str_replace(".", "_", $if);
	if (strlen($vlanif) > IF_NAMESIZE) {
		logger(LOG_ERR, localize_text("%s interface name too big %s. (max. size: %d).",
		    "interface_qinq2_configure", $vlanif, IF_NAMESIZE));
		return;
	}

	exec("/sbin/ifconfig vlan create vlandev {$if} vlan {$tag} name {$vlanif}");

	return $vlanif;
}
