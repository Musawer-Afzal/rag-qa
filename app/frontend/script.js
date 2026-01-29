let currentDoc = null;

async function upload() {
    const fileInput = document.getElementById("file");
    const file = fileInput.files[0];

    if (!file) {
        alert("Please select a file");
        return;
    }

    const form = new FormData();
    form.append("file", file);

    document.getElementById("answer").innerText = "⏳ Processing document...";

    const res = await fetch("http://localhost:8000/upload", {
        method: "POST",
        body: form
    });

    const data = await res.json();

    if (data.error) {
        alert(data.error);
        return;
    }

    currentDoc = data.doc_name;
    document.getElementById("answer").innerText = "✅ Uploaded: " + currentDoc;
}

async function ask() {
    const q = document.getElementById("question").value;

    if (!currentDoc) {
        alert("Upload a document first");
        return;
    }

    document.getElementById("answer").innerText = "🤔 Thinking...";

    const res = await fetch("http://localhost:8000/qa/ask", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
            doc_name: currentDoc,
            question: q
        })
    });

    const data = await res.json();

    document.getElementById("answer").innerText =
        JSON.stringify(data.answers, null, 2);
}