<?php
session_start();
if($_SESSION['email']&&isset($_SESSION['email'])&$_SESSION['login']==1){

}else{
    header("location:login.php");
}

?>
<br>
<head>
    <script src="jquery-3.3.1.min.js"></script>
    <link rel="stylesheet" href="css/main.css" type="text/css">
    <link rel="stylesheet" href="css/history.css" type="text/css">

</head>
<button  onclick="location.href='login.php?logout=true'">logout</button>

<button  onclick="historyf()">history</button>
<script>
    function historyf(){
        var url = 'history.php';
        document.getElementById('hisTable').innerHTML='';
        if( $('#history').is(":visible")){
            $('#history').hide();
            return;
        }

        $('#history').show();
        $.ajax({
            type: "POST",
            url: url,
            data:"", // serializes the form's elements.
            success: function(data)
            {
                var parent = $("#hisTable");
                var obj = JSON.parse(data);



                $('#hisTable').append("<tr> <th>DRUG</th> <th>ADR</th></tr>");



                obj.forEach(function (element){
                    var chil = document.createElement("tr");
                    chil.className="hisRow";
                    var chtd1 = document.createElement("td");
                    chtd1.className="hisCol";
                    var link1 = document.createElement("a");
                    link1.href='javascript:func1("'+element[0]+'","'+element[1] +'");';
                    link1.textContent = element[0];
                    var link2 = document.createElement("a");
                    link2.href='javascript:func1("'+element[0]+'","'+element[1] +'");';
                    link2.textContent = element[1];
                    chtd1.appendChild(link1);
                    var chtd2 = document.createElement("td");
                    chtd2.className="hisCol";
                    chtd2.appendChild(link2);
                    chil.appendChild(chtd1);
                    chil.appendChild(chtd2);

                    document.getElementById('hisTable').appendChild(chil);
                })




            }
        });

    }
    function func1(drug,adr) {
        var url = "search2.php"; // the script where you handle the form input.
        $("#load").show();
        var datat = "drug="+drug+"&adr="+adr;
        $.ajax({
            type: "POST",
            url: url,
            data: datat, // serializes the form's elements.
            success: function(data)
            {
                if(data.search("okrrlyc")!=-1){
                    var td = drug.replace(/ /g,'_');
                    var ta = adr.replace(/ /g,'_');
                    //succ
                    document.getElementById("ifram").src="vis.php?fileName="+td+"_"+ta;
                    //document.getElementById("ifram").contentDocument.location.reload(true);
                    //document.getElementById("ifram").scrollIntoView({  behavior: "smooth", block: "start" });
                    $('html, body').animate({
                        scrollTop: $("#ifram").offset().top
                    }, 600);
                }else{
                    //fail
                    alert("sorry there is no proper data for this pair of ADR and Drug");
                }

                $("#load").hide();
                $('#history').hide();
            }
        });
    }

</script>

<div class="history" id="history" hidden="hidden">
<table id="hisTable">
</table>
</div>
</br>
<div>
<h1 class="h1">Search</h1>


<div class="flexsearch">
    <div class="flexsearch--wrapper">

        <form id="formSearch" class="flexsearch--form"  method="post">

            <div class="flexsearch--input-wrapper">
                <input class="flexsearch--input" type="search" placeholder="drug" name="drug">
            </div>
            <input class="flexsearch--submit" type="submit" value="&#10140;"/>
            <div class="flexsearch--input-wrapper">
                <input class="flexsearch--input" type="search" placeholder="side effect" name="adr">
                <input class="flexsearch--submit2" type="submit" value="&#10140;"/>
            </div>

        </form>
    </div>
</div>
    <div style="display:block ;  position: relative">

    <iframe id="ifram" width="100%" frameborder="0" height="100%" src="vis.html"></iframe>
    <script >
        $("#formSearch").submit(function(e) {
            e.preventDefault(); // avoid to execute the actual submit of the form.

            var url = "search.php"; // the script where you handle the form input.
            var drug = this.drug.value;
            var adr = this.adr.value;
           if(drug==''){

               if(adr==''){
                   alert("ADR and Drug should not be empty");
                   return false;
               }
               alert("Drug should not be empty");
                return false;
           }
           if(adr==''){
               alert("ADR should not be empty");
               return false;
           }
            $("#load").show();
            var datat =$("#formSearch").serialize();

            $.ajax({
                type: "POST",
                url: url,
                data: datat, // serializes the form's elements.
                success: function(data)
                {
                    if(data.search("okrrlyc")!=-1){
                        //succ
                        var tempD = drug.replace(/ /g,'_');
                        var tempA = adr.replace(/ /g,'_');
                        document.getElementById("ifram").src="vis.php?fileName="+tempD+"_"+tempA;
                        //document.getElementById("ifram").contentDocument.location.reload(true);
                        //document.getElementById("ifram").scrollIntoView({  behavior: "smooth", block: "start" });
                        $('html, body').animate({
                            scrollTop: $("#ifram").offset().top
                        }, 600);
                    }else{
                        //fail
                        alert("sorry there is no proper data for this pair of ADR and Drug");
                    }

                    $("#load").hide();

                }
            });

        });
    </script>
        <div class="loader" id="load" hidden="hidden"></div>


    </div>
</div>


</html>
