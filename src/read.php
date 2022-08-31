<?php
header("Content-Type: text/html");

$blacklist = "none";

$param = $_GET["content"];

if (strpos($param, $blacklist) !== false)
{

    echo "</br>blacklisted";
    exit;

}
else
{
    $param = str_ireplace($blacklist, "", $param);
    $fp = fopen('test.html', 'w') or die("unable to open file");
    fwrite($fp, $param);
    fclose($fp);

}

$html_file_url = 'test.html';
$pdf_file_url = 'test.pdf';
$cmd = "xvfb-run wkhtmltopdf --allow / $html_file_url $pdf_file_url";
shell_exec($cmd);
$file = 'test.pdf';
$filename = 'test.pdf';

header('Content-type: application/pdf');
header('Content-Disposition: inline; filename="' . $filename . '"');
header('Content-Transfer-Encoding: binary');
header('Content-Length: ' . filesize($file));
header('Accept-Ranges: bytes');

@readfile($file);
?>
