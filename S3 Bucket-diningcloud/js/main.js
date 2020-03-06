var apigClient = apigClientFactory.newClient();
var messages = [], //array that hold the record of each string in chat
	lastUserMessage = "", //keeps track of the most recent input string from the user
	botMessage = "", //var keeps track of what the chatbot is going to say
	talking = true; //when false the speach function doesn't work

function chatbotResponse() {
	// User's own message for display
	lastUserMessage = userMessage();

	return new Promise(function (resolve, reject) {
		talking = true;
		let params = {};
		var additionalParams = {};
		var body = {
			"messages": lastUserMessage
		}
		apigClient.chatbotPost(params, body, additionalParams)
			.then(function (result) {
				debugger;
				reply = result.data.body;

				$("<li class='replies'><p>" + reply + "</p></li>").appendTo($('.messages ul'));
				$('.message-input input').val(null);
				$('.contact.active .preview').html('<span>You: </span>' + reply);
				$(".messages").animate({ scrollTop: 20000000 }, "slow");
				resolve(result.data.body);
				botMessage = result.data.body;
			}).catch(function (result) {
				// Add error callback code here.
				console.log(result);
				botMessage = "Couldn't connect"
				reject(result);
			});
	})
	$(".messages").animate({ scrollTop: 20000000 }, "slow");
}

//Js for the chat application

$(".messages").animate({ scrollTop: 20000000 }, "slow");

function userMessage() {
	message = $(".message-input input").val();
	if ($.trim(message) == '') {
		return null;
	}

	$('<li class="sent"><p>' + message + '</p></li>').appendTo($('.messages ul'));
	$('.message-input input').val(null);
	$('.contact.active .preview').html('<span>You: </span>' + message);
	$(".messages").animate({ scrollTop: 20000000 }, "slow");
	return message;
};

$('.submit').click(function () {
	chatbotResponse();
});

$(window).on('keydown', function (e) {
	//debugger;
	if (e.which == 13) {
		chatbotResponse();
		return false;
	}
});