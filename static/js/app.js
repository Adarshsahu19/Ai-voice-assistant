const state = {
    sessionId: null,
    muted: false,
    listening: false,
    recognition: null,
};

const elements = {
    messages: document.getElementById("messages"),
    promptInput: document.getElementById("promptInput"),
    composerForm: document.getElementById("composerForm"),
    listenBtn: document.getElementById("listenBtn"),
    sendBtn: document.getElementById("sendBtn"),
    muteBtn: document.getElementById("muteBtn"),
    newSessionBtn: document.getElementById("newSessionBtn"),
    providerMode: document.getElementById("providerMode"),
    chips: Array.from(document.querySelectorAll(".chip")),
};

function addMessage(role, content) {
    const wrapper = document.createElement("article");
    wrapper.className = `message ${role}`;

    const meta = document.createElement("span");
    meta.className = "meta";
    meta.textContent = role === "assistant" ? "ASSISTANT" : "YOU";

    const text = document.createElement("div");
    text.textContent = content;

    wrapper.append(meta, text);
    elements.messages.appendChild(wrapper);
    elements.messages.scrollTop = elements.messages.scrollHeight;
}

function speak(text) {
    if (state.muted || !("speechSynthesis" in window)) {
        return;
    }

    const utterance = new SpeechSynthesisUtterance(text);
    utterance.rate = 1;
    utterance.pitch = 1;
    utterance.lang = "en-US";
    window.speechSynthesis.cancel();
    window.speechSynthesis.speak(utterance);
}

async function createSession() {
    const response = await fetch("/api/session", { method: "POST" });
    const data = await response.json();
    state.sessionId = data.session_id;
}

async function sendMessage(message) {
    if (!message.trim()) {
        return;
    }

    addMessage("user", message);
    elements.promptInput.value = "";
    elements.sendBtn.disabled = true;

    try {
        const response = await fetch("/api/assistant/message", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                session_id: state.sessionId,
                message,
            }),
        });

        if (!response.ok) {
            throw new Error("Request failed");
        }

        const data = await response.json();
        elements.providerMode.textContent = data.provider_mode;
        addMessage("assistant", data.reply);
        speak(data.reply);
    } catch (error) {
        addMessage("assistant", "The assistant could not complete that request. Check the backend and try again.");
    } finally {
        elements.sendBtn.disabled = false;
    }
}

function setListening(enabled) {
    state.listening = enabled;
    elements.listenBtn.textContent = enabled ? "Stop Listening" : "Start Listening";
    elements.listenBtn.classList.toggle("listening", enabled);
}

function initSpeechRecognition() {
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    if (!SpeechRecognition) {
        elements.listenBtn.disabled = true;
        elements.listenBtn.textContent = "Voice Unsupported";
        addMessage("assistant", "Speech recognition is not available in this browser. You can still type messages.");
        return;
    }

    const recognition = new SpeechRecognition();
    recognition.lang = "en-US";
    recognition.continuous = false;
    recognition.interimResults = false;

    recognition.onstart = () => setListening(true);
    recognition.onend = () => setListening(false);
    recognition.onerror = () => setListening(false);
    recognition.onresult = (event) => {
        const transcript = event.results[0][0].transcript;
        elements.promptInput.value = transcript;
        sendMessage(transcript);
    };

    state.recognition = recognition;
}

async function resetSession() {
    await createSession();
    elements.messages.innerHTML = "";
    addMessage(
        "assistant",
        "New session ready. Speak or type a request. I can reply aloud and keep context inside this session."
    );
}

elements.composerForm.addEventListener("submit", async (event) => {
    event.preventDefault();
    await sendMessage(elements.promptInput.value);
});

elements.listenBtn.addEventListener("click", () => {
    if (!state.recognition) {
        return;
    }

    if (state.listening) {
        state.recognition.stop();
        return;
    }

    state.recognition.start();
});

elements.muteBtn.addEventListener("click", () => {
    state.muted = !state.muted;
    elements.muteBtn.textContent = state.muted ? "Unmute Voice" : "Mute Voice";
    if (state.muted) {
        window.speechSynthesis.cancel();
    }
});

elements.newSessionBtn.addEventListener("click", resetSession);

elements.chips.forEach((chip) => {
    chip.addEventListener("click", async () => {
        await sendMessage(chip.dataset.prompt || "");
    });
});

window.addEventListener("DOMContentLoaded", async () => {
    await createSession();
    initSpeechRecognition();
    addMessage(
        "assistant",
        "Voice Assistant Studio is live. Try asking for the time, a plan, or a quick summary."
    );
});
