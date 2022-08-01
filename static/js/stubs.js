$(document).ready(function(){
   let selected = "";
//       $("#openDialog").click(function(){
//         $.ajax({
//           url:`/get_folders`,
//           method:"GET",
////           data:{'name': 'SelectFolder', 'selectedDrive': selectedDrives},
//
//             beforeSend:function()
//             {
//               $('#openDialog').attr('disabled', 'disabled');
//               $('#option').attr('disabled', 'disabled');
//               $('#save').attr('disabled', 'disabled');
//             },
//             success:function(data)
//             {
//               $('#folderPath').val(data)
//               $('#save').attr('disabled', false);
//               $('#option').attr('disabled', false);
//               $('#openDialog').attr('disabled', false);
//             }
//           })
//       });

       $("#option").click(function(e){
         alert("clicked");
         selected = textValue;
       })
 
       const option = document.getElementById("option");
       $('#login_form').on('submit', function(event){
         event.preventDefault();
 
         console.log("event is ", $('#username').val());
         console.log("event is ", $('#password').val());
         console.log("event is ", $(this).serialize());
 
             const content = {
                     "username":$('#username').val().toString(),
                     "password":$('#password').val().toString()
              }
             fetch("/login",{
                 method:"POST",
                 headers:{
                     'Content-Type':'application/json'
                 },
                 body:JSON.stringify(content)
             })
             .then(function(response){
                if(response.status != 200){
                     return "Response status code was not 200"
                }
                return "correct"
             })
             .catch(error => console.log(error))
       })
 
      $('#stub_form').on('submit', function(event){
        event.preventDefault();
        var count_error = 0;
        if($('#folderPath').val() == '')
        {
         $('#folderPath_error').text('Folder Path is required to Separate/Deletion Archived');
         count_error++;
        }
        else
        {
         $('#folderPath_error').text('');
        }
        if(count_error == 0)
        {
         $.ajax({
            url:"/ajaxmovestubs",
            method:"POST",
            data:$(this).serialize(),
            beforeSend:function()
         {
             $('#save').attr('disabled', 'disabled');
             $('#process').css('display', 'block');
         },
         success:function(data)
         {
         //console.log("data", data);
             var percentage = 0;
             var timer = setInterval(function(){
             percentage = percentage + 20;
             progress_bar_process(percentage, timer,data);
         }, 1000);
        }
       })
        }
        else
        {
         return false;
        }
       });
        
        //confirm call
     $('#stub_confirm_form').on('submit', function(event){
        event.preventDefault();
        var count_error = 0;
         
        if($('#folderPath').val() == '')
        {
         $('#folderPath_error').text('Folder Path is required to Separate/Deletion Archived');
         count_error++;
        }
        else
        {
         $('#folderPath_error').text('');
        }
 
        if(count_error == 0)
        {
         $.ajax({
            url:"/stubsconfirm",
            method:"POST",
            data:$(this).serialize(),
            beforeSend:function()
         {
             $('#Confirm').attr('disabled', 'disabled');
             $('#Cancel').css('display', 'block');
              $('#process').css('display', 'block');
         },
         success:function(data)
         { 
             var percentage = 0;
             var timer = setInterval(function(){
             percentage = percentage + 20;
             progress_bar_process_confirm(percentage, timer,data);
         }, 1000);
             
        }
       })
        }
        else
        {
         return false;
        }
 
       });
       function progress_bar_process(percentage, timer,data)
       {
      $('.progress-bar').css('width', percentage + '%');
      if(percentage > 100)
      {
       clearInterval(timer);
       $('#stub_form')[0].reset();
       $('#process').css('display', 'none');
       $('.progress-bar').css('width', '0%');
       $('#save').attr('disabled', false);
       $('#success_message').html(data['msg']);
       $('#data').val(data);
       $('#id_frm_ajx')[0].submit();
       setTimeout(function(){
        $('#success_message').html('');
       }, 5000);
      }
       }
 
     
     
     function progress_bar_process_confirm(percentage, timer,data)
     {
      $('.progress-bar').css('width', percentage + '%');
      if(percentage > 100)
      {
       clearInterval(timer);
       $('#stub_confirm_form')[0].reset();
       $('#Cancel').css('display', 'none');
       $('.progress-bar').css('width', '0%');
       $('#Confirm').css('display', 'none');
       $('#process').css('display', 'none');
          
       $('#success_message').html(data['msg']);
       $('#success_message_confirm').html("<div class='alert alert-success'><strong>Deletion Process has been completed successfully </strong></div><a href='/' class='btn btn-primary' id='Cancel'>Back to home</a>");
       //$('#data').val(data);
       //$('#id_frm_ajx')[0].submit();
       setTimeout(function(){
        $('#success_message').html('');
       }, 5000);
      }
       }
 
      });
      setTimeout(function(){
        $('#message').fadeOut('slow')
      },4000) 
      // setTimeout(function(){
      //   $('#optProc').html("<div class='alert alert-success'><strong>seperation Process has been completed successfully </strong></div>").fadeOut('slow')
      // },4000) 