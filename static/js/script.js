// The URL of the API endpoint
const BASE_URI = "http://127.0.0.1:5000";

let state = {
  gpt: 0,
  gpt_choice: "",
  user_choice: "",
  round: 0,
  user: 0,
  conversation: [],
  selected_choice: "",
};

// Elements on page
// Trash talk section
const submit_trash_talk = document.getElementById("trash-talk-submit");
const trashTalkInputElement = document.getElementById("user-trash-talk");
const chatBox = document.getElementById("chat-box");

// Event listeners
submit_trash_talk.addEventListener("click", (e) => {
  e.preventDefault();
  submitUserTrashTalk();
});

trashTalkInputElement.addEventListener("keydown", (e) => {
  if (e.key === "Enter") {
    submitUserTrashTalk();
  }
});

// Functions to handle submissions
let submitUserTrashTalk = () => {
  // Get user trash talk
  let user_trash_talk = trashTalkInputElement.value;

  // Update chat with User comment
  updateChat("user", user_trash_talk);
  // Clear the input element after submission
  trashTalkInputElement.value = "";

  // Prep data to send to server
  let data = {
    user_comment: user_trash_talk,
  };
  // send to server and update chat.
  // This function call has a side effect of
  // updating the chat UI with a response
  makePostApiCall("/chat", data);
};

// Utility Functions
let makePostApiCall = (path, data) => {
  let payload = {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(data),
  };

  fetch(BASE_URI + path, payload)
    .then((response) => {
      if (!response.ok) {
        throw new Error("Network response was not ok");
      }
      return response.json();
    })
    .then((data) => {
      if (path === "/chat") {
        // Update the Chat
        console.log("Response from server('/chat'):", data);
        updateChat("gpt", data.trash_talk);
      }
    })
    .catch((error) => {
      console.error("There was a problem with the fetch operation:", error);
    });
};

let loadCurrentChat = () => {
  let convoData = JSON.parse(chatBox.getAttribute("data-conversation"));
  convoData.forEach((element) => {
    let chatElement = makeChatWrapper(element.who, element.comment);
    chatBox.prepend(chatElement);
  });
};

let updateChat = (who, comment) => {
  let chatElement = makeChatWrapper(who, comment);
  chatBox.prepend(chatElement);
};

let makeChatWrapper = (who, comment) => {
  // Create wrapper
  let chatWrapper = document.createElement("span");
  chatWrapper.setAttribute("class", "chat-text-wrapper");
  // Make who element
  let whoElement = document.createElement("b");
  whoElement.textContent = who + ":";
  if (who === "user") {
    whoElement.style.color = "blue";
  }
  // Make comment element
  let commentElement = document.createElement("span");
  commentElement.setAttribute("class", "chat-text");
  commentElement.textContent = htmlDecode(comment);

  // Append all the children
  chatWrapper.appendChild(whoElement);
  chatWrapper.appendChild(commentElement);

  return chatWrapper;
};

function htmlDecode(input) {
  var doc = new DOMParser().parseFromString(input, "text/html");
  console.log(doc.documentElement.textContent);
  return doc.documentElement.textContent;
}

// Main entrypoint (all the setup stuff happens here)
let main = () => {
  loadCurrentChat();
};

main();
