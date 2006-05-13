<p id="trail">
Trail: <a href="/">Home</a> &gt;
<?php
$self = $_SERVER['PHP_SELF'];
if (substr($self, 0, 6) == "/info/" && substr($self, -10) != "index.html") {
?>
<a href="/info/">Information Repository</a> &gt;
<?php
}
?>
</p>
