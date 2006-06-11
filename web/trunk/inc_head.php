<?php
// $Id$
?>
<link rel="stylesheet" type="text/css" href="/refit.css">
<link rel="stylesheet" type="text/css" media="print" href="/print.css">
<?php
if (!($section == "main" && $index_html)) {
?>
<link rel="start" href="/" title="Home">
<?php
}
if ($section == "doc") {
  if ($nextdocpage) {
    print '<link rel="next" href="'.$nextdocpage[0].'" title="'.$nextdocpage[1].'">'."\n";
  }
  if ($prevdocpage) {
    print '<link rel="prev" href="'.$prevdocpage[0].'" title="'.$prevdocpage[1].'">'."\n";
  }
  if (!$index_html) {
    print '<link rel="up" href="index.html" title="Contents">'."\n";
  }
}
?>
<link rel="icon" href="/favicon.ico" type="image/x-icon">
<link rel="shortcut icon" href="/favicon.ico" type="image/x-icon">
