async function upload() {
    const file = document.getElementById("file").files[0];
    const form = new FormData();
    form.append("file", file);

    await fetch("http://localhost:8000/documents/upload", {
        method: "POST",
        body: form
    });

    alert("Uploaded!");
}

async function ask() {
    const q = document.getElementById("question").value;

    const res = await fetch("http://localhost:8000/qa/ask", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ question: q })
    });

    const data = await res.json();
    document.getElementById("answer").innerText = data.answer;
}