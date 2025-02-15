var sliderIndex = 1;
showSlides(sliderIndex);

function plusSlides(n){
  showSlides(sliderIndex += n)
}

function showSlides(n){
  let slider = document.getElementsByClassName("slider");

  if(n > slider.length){
    sliderIndex = 1
  }
  if(n < 1){
    sliderIndex = slider.length
  }

  for(i = 0; i < slider.length; i++){
    slider[i].style.display = "none";
  }

  slider[sliderIndex - 1].style.display = "block";
}

document.addEventListener('DOMContentLoaded', function() {
  const chatBody = document.getElementById('chatBody');
  const chatInput = document.getElementById('chatInput');
  const sendChatBtn = document.getElementById('sendChatBtn');

  function addMessage(text, sender) {
      const messageDiv = document.createElement('div');
      messageDiv.classList.add('chat-message');
      messageDiv.classList.add(sender === 'bot' ? 'bot-message' : 'user-message');
      messageDiv.innerText = text;
      chatBody.appendChild(messageDiv);
      chatBody.scrollTop = chatBody.scrollHeight; // Auto-scroll
  }

  sendChatBtn.addEventListener('click', function() {
      const userMessage = chatInput.value.trim();
      if (userMessage === '') return;

      addMessage(userMessage, 'user');
      chatInput.value = '';

      fetch('/chatbot', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ message: userMessage })
      })
      .then(response => response.json())
      .then(data => {
          addMessage(data.reply, 'bot');
      })
      .catch(error => {
          addMessage('Error: Unable to process request.', 'bot');
          console.error(error);
      });
  });

  chatInput.addEventListener('keypress', function(event) {
      if (event.key === 'Enter') {
          sendChatBtn.click();
      }
  });
});
