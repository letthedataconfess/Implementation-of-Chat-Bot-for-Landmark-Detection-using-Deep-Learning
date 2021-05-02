 $('#my-chat-layout-base').data('hideChatWindow',true); 

var timestamp_session_id = new Date().getTime();

function setTimestamp() {
  timestamp_session_id = new Date().getTime();
}

function getTimestamp() {
  return timestamp_session_id;
}

function minimiseChatBox() {

  var _hideChatWindow = $('#my-chat-layout-base').data('hideChatWindow'); 

  if(_hideChatWindow) {
    
    $("#my-chat-layout-base").height("45px");
    $(".mdl-mini-footer").css('display','none');
    $('#my-chat-layout-base').data('hideChatWindow',false); 

  } else {

    $("#my-chat-layout-base").height("400px");
    $(".mdl-mini-footer").css('display','block');

    $('#my-chat-layout-base').data('hideChatWindow',true); 
  }

}


function userQuery(input_message, bot_flag) {

  var userQueryValue = $("#myInputChatText").val();

  if(input_message) {
    userQueryValue = input_message;
  }

  if(userQueryValue.trim()) {
    userQueryValue = userQueryValue.trim();

    var myKeyVals = {
      "query": userQueryValue,
      "session_id": getTimestamp()
    };

    if(bot_flag) {
      console.log("No input from user, its bot");
    } else {
      var userInputHtml = '<li tabindex="1" class="mdl-list__item mdl-menu__item--full-bleed-divider font-size-20px"><span class="mdl-list__item-primary-content"><i class="material-icons mdl-list__item-avatar display_hidden"></i><span class="mdl-list__item-text-body text_align_right text_user_input"> ' + userQueryValue + '</span></span><span class="mdl-list__item-secondary-content"><i class="material-icons mdl-list__item-avatar">person</i></span></li>';

      $("#message-list").append(userInputHtml);
      $('#message-list li:last').focus();
    }
    

    $.ajax({
          type: 'POST',
          url: "/api_ai_test",
          contentType: "application/json",
          data: JSON.stringify(myKeyVals),
          dataType: "json",
          error: function() {
            alert("Something went wrong, please try later"); 
          },
          success: function(resultData) { 
            console.log(resultData);

            var outputHTML = '<li tabindex="1" class="mdl-list__item mdl-menu__item--full-bleed-divider font-size-20px"><span class="mdl-list__item-primary-content"><i class="material-icons mdl-list__item-avatar">adb</i><span class="mdl-list__item-text-body text_bot_output">' + resultData["message"] + '</span></span><span class="mdl-list__item-secondary-content display_hidden"></span></li>';
          
           
            if(resultData["top_3_liked_movies"] && resultData["top_3_recommended_movies"]) {
              var top_3_liked_movies = "<b>Favourite movies of user:</b> <br>";
              var top_3_recommended_movies = "<b>Recommended movies:</b> <br>";

              for (x in resultData["top_3_liked_movies"]) {
                  top_3_liked_movies = top_3_liked_movies + "- " + resultData["top_3_liked_movies"][x] + "<br>";
              }

              for (x in resultData["top_3_recommended_movies"]) {
                  top_3_recommended_movies = top_3_recommended_movies + "- " + resultData["top_3_recommended_movies"][x] + "<br>";
              }

              outputHTML = '<li tabindex="1" class="mdl-list__item mdl-menu__item--full-bleed-divider font-size-20px"><span class="mdl-list__item-primary-content"><i class="material-icons mdl-list__item-avatar">adb</i><span class="mdl-list__item-text-body text_bot_output">' + top_3_liked_movies + "<br>" + top_3_recommended_movies + '</span></span><span class="mdl-list__item-secondary-content display_hidden"></span></li>';
            }

            $("#message-list").append(outputHTML);
            $('#message-list li:last').focus();            
            $("#myInputChatText").focus();

         

            if(resultData["session_refresh"]) {
              setTimestamp();
            }
          }
      });
  }

  $("#myInputChatText").val("");        
  $("#myInputChatText").focus();

  return false;
}