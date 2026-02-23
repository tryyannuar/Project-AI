const chatBox = document.getElementById("chatBox");
const userInput = document.getElementById("userInput");

function createMessage(role, text) {
  const message = document.createElement("div");
  message.className = `message ${role}`;

  const content = document.createElement("div");
  content.className = "message-content";

  const avatar = document.createElement("img");
  avatar.className = "avatar";
  avatar.src = role === "bot"
    ? "/static/focalors.png"
    : "/static/user.png";

  const bubble = document.createElement("div");
  bubble.className = "bubble";
  bubble.textContent = text;

  content.appendChild(avatar);
  content.appendChild(bubble);
  message.appendChild(content);

  chatBox.appendChild(message);

  // auto scroll
  chatBox.scrollTop = chatBox.scrollHeight;
}

async function sendMessage() {
  const text = userInput.value.trim();
  if (!text) return;

  createMessage("user", text);
  userInput.value = "";
  userInput.disabled = true;

  try {
    const response = await fetch("/chat", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({ message: text })
    });

    if (!response.ok) {
      throw new Error("Server error");
    }

    const data = await response.json();
    createMessage("bot", data.reply);

  } catch (error) {
    createMessage("bot", "Terjadi kesalahan koneksi.");
  } finally {
    userInput.disabled = false;
    userInput.focus();
  }
}

// kirim dengan Enter
userInput.addEventListener("keydown", function(e) {
  if (e.key === "Enter") {
    sendMessage();
  }
});

// Pesan awal
createMessage(
  "bot",
  "Selamat datang. Jangan gugup. Aku memang terlihat luar biasa, tapi aku tidak menggigit… kecuali kamu membosankan."
);
