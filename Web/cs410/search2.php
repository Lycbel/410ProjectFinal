<?php
session_start();
$adr =$_POST['adr'];
$drug =$_POST['drug'];
$adro =$_POST['adr'];
$drugo =$_POST['drug'];
$adr = str_replace(' ','_',$adr);
$drug = str_replace(' ','_',$drug);
$last_line=system("python generateGraph.py ".$drug." ".$adr,$result);
echo ($last_line);
if($last_line=='1'){
    if(isset($_SESSION['email']))
        addHistory($adro,$drugo,$_SESSION['email']);
    else{
        echo("no history");
    }

    echo("okrrlyc");
}else{
    echo($last_line);
}
function connect(){
    $servername = "localhost";
    $username = "root";
    $password = "";
    $dbname = "cs410";

// Create connection
    $conn = new mysqli($servername, $username, $password,$dbname);

// Check connection
    if ($conn->connect_error) {
        die("Connection failed: " . $conn->connect_error);
    }
    return $conn;
}
function addHistory($adr,$drug,$email){

}

?>