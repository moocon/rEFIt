<?php
// $Id$

$self = $_SERVER['PHP_SELF'];
$selfname = substr($self, strrpos($self, "/") + 1);

$section = "main";
if (substr($self, 0, 6) == "/info/")
  $section = "info";
if (substr($self, 0, 5) == "/doc/")
  $section = "doc";
$index_html = 0;
if ($selfname == "index.html")
  $index_html = 1;

?>
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">
