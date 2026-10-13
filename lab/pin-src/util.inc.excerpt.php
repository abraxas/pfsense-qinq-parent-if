<?php
/* Pin excerpt pfsense/pfsense 9363ac5b8651a1c7a333180425ce7719070f95f9. Do not edit by hand. */

function is_numericint($arg) {
	return (((is_int($arg) && $arg >= 0) || (is_string($arg) && strlen($arg) > 0 && ctype_digit(strval($arg)))) ? true : false);
}
function is_intrange($range, $min, $max) {
	$values = preg_split("/[:-]/", $range);

	if (!is_array($values) || count($values) != 2) {
		return false;
	}

	if (!ctype_digit(strval($values[0])) || !ctype_digit(strval($values[1]))) {
		return false;
	}

	$values[0] = intval($values[0]);
	$values[1] = intval($values[1]);

	if ($values[0] >= $values[1]) {
		return false;
	}

	if ($values[0] < $min || $values[1] > $max) {
		return false;
	}

	return true;
}

