
<html>
<head>
<script src="jquery-3.3.1.min.js"></script>
<link rel="stylesheet" href="css/login.css" type="text/css">

</head>
<?php
session_start();
if(isset($_SESSION['login'])){
    if(isset($_REQUEST['logout'])){
        $_SESSION['login']=null;
    }
    else {
        header("location:main.php");
        return;
    }
}
if(isset($_REQUEST["registerM"])) {
    $dd=$_REQUEST["registerM"];
    ?>
    <div class="message">
       <?php echo($dd); ?>
    </div>
    <?php
}
?>
<div class="login-page">
  <div class="form">
    <form class="register-form" action="auth.php?type=2">
      <input type="text" placeholder="name" name = "name"/>
      <input type="password" placeholder="password" name ="pass"/>
      <input type="text" placeholder="email address" name="email"/>
<input hidden="hidden" name="type" value="2">
      <button>create</button>
      <p class="message">Already registered? <a href="#">Sign In</a></p>
    </form>
    <form class="login-form" action="auth.php?type=1">
      <input type="text" placeholder="username" name="email"/>
      <input type="password" placeholder="password" name="pass"/>
<input hidden="hidden" name="type" value="1">
      <button>login</button>
      <p class="message">Not registered? <a href="#">Create an account</a></p>
    </form>
  </div>
</div>
<script>
$('.message a').click(function(){
   $('form').animate({height: "toggle", opacity: "toggle"}, "slow");
});
</script>
</html>