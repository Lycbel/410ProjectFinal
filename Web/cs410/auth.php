<?php
connect();
if(isset($_REQUEST['type'])){
    $type = $_REQUEST['type'];
    if($type==1){
        $pass = $_REQUEST['pass'];
        $email = $_REQUEST['email'];
        login($email,$pass);

    }else if($type==2){
        $pass = $_REQUEST['pass'];
        $email = $_REQUEST['email'];
        $name = $_REQUEST['name'];
        register($email,$pass,$name);
    }


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
function login($email,$pass){
    $conn = connect();
    $stmt = $conn->prepare("select email from  user where email=? and pass=?");
    $stmt->bind_param("ss",  $email, $pass);
    if(!$stmt->execute()){
        echo("error");
    }
    $stmt->bind_result($district);
    $stmt->fetch();
    if(isset($district)){
        session_start();
        $_SESSION["login"]=1;
        $_SESSION["email"] = $email;
        header("location:main.php");
    }else{
        header("location:login.php?registerM="."login failed");
    }

    $stmt->close();
    $conn->close();
}
function register($email,$pass,$name){
    $conn = connect();
    $code = checkUser($email);
    if($code==1){
        header("location:login.php?registerM="."email already in use");
        return;
    }
    if(code == 2){
        header("location:login.php?registerM="."register error");
        return;
    }

    $stmt = $conn->prepare("INSERT INTO user (name, email, pass) VALUES (?, ?, ?)");
    $stmt->bind_param("sss", $name, $email, $pass);
    if($stmt->execute()){
        header("location:login.php?registerM="."register successfully");
    }else{
        header("location:login.php?registerM="."register error");
    }
    $stmt->close();
    $conn->close();
}
//0 ok 1 exist 2 error
function checkUser($email){
    $conn = connect();
    $stmt = $conn->prepare("select email from  user where email=? ");
    $stmt->bind_param("s",  $email);
    if(!$stmt->execute()){
        return 2;
    }
    $stmt->bind_result($district);
    $stmt->fetch();
    if(isset($district)){
        return 1;
    }else{
        return 0;
    }
    $stmt->close();
    $conn->close();
}




?>