let fetchController = null;

function displayResults(data) {
  const loadingOverlay = document.getElementById('loading-overlay');
  const analysisResultsContainer = document.getElementById('analysis-results-container');
  const headingContainer = document.getElementById("heading-container");
  const percentageContainer = document.getElementById("percentage-container");
  const briefInfoContainer = document.getElementById("brief-info-container");
  const reasoningContainer = document.getElementById("reasoning-container");
  const sourcesContainer = document.getElementById("sources-container");
  const resultsContainer = document.getElementById("results-container");

  loadingOverlay.style.display = 'none';
  analysisResultsContainer.style.display = 'block';

  headingContainer.innerHTML = "";
  percentageContainer.innerHTML = "";
  briefInfoContainer.innerHTML = "";
  reasoningContainer.innerHTML = "";
  sourcesContainer.innerHTML = "";
  resultsContainer.innerHTML = "";

  if (data.error) {
    analysisResultsContainer.style.display = 'none';
    resultsContainer.innerHTML = `<p>Error: ${data.error}</p>`;
  } else if (data.heading && data.percentage !== undefined && data.brief_info !== undefined && data.sources !== undefined) {
    headingContainer.innerHTML = data.heading;
    percentageContainer.innerHTML = `${data.percentage}%`;
    briefInfoContainer.innerHTML = `<p>${data.brief_info}</p>`;
    reasoningContainer.innerHTML = `<p>${data.reasoning}</p>`;

    if (data.sources.length > 0) {
      let sourcesHtml = `<h3>Sources:</h3><ul>`;
      data.sources.forEach(source => {
        sourcesHtml += `<li><a href="${source}" target="_blank">${source}</a></li>`;
      });
      sourcesHtml += `</ul>`;
      sourcesContainer.innerHTML = sourcesHtml;
    } else {
      sourcesContainer.innerHTML = `<p>No specific sources found.</p>`;
    }
  } else {
    resultsContainer.innerHTML = "<p>Unexpected analysis format.</p>";
    console.error("Unexpected analysis format:", data);
  }
}

function fetchAnalysis(text, url, model) {
  if (fetchController) {
    fetchController.abort();
  }
  fetchController = new AbortController();
  const signal = fetchController.signal;

  const loadingOverlay = document.getElementById('loading-overlay');
  const analysisResultsContainer = document.getElementById('analysis-results-container');

  loadingOverlay.style.display = 'flex';
  analysisResultsContainer.style.display = 'none';

  fetch("/api/analyze", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ text: text, url: url, model: model }),
    signal
  })
  .then(response => response.json())
  .then(analysis => {
    displayResults(analysis);
  })
  .catch(error => {
    if (error.name === 'AbortError') {
      console.log('Fetch aborted');
    } else {
      console.error("Error:", error);
      displayResults({ error: "Could not connect to the backend." });
    }
  });
}

function fetchImageAnalysis(imageData, url, model) {
  if (fetchController) {
    fetchController.abort();
  }
  fetchController = new AbortController();
  const signal = fetchController.signal;

  const loadingOverlay = document.getElementById('loading-overlay');
  const analysisResultsContainer = document.getElementById('analysis-results-container');

  loadingOverlay.style.display = 'flex';
  analysisResultsContainer.style.display = 'none';

  fetch("/api/analyze_image", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ image: imageData, url: url, model: model }),
    signal
  })
  .then(response => response.json())
  .then(analysis => {
    displayResults(analysis);
  })
  .catch(error => {
    if (error.name === 'AbortError') {
      console.log('Fetch aborted');
    } else {
      console.error("Error:", error);
      displayResults({ error: "Could not connect to the backend." });
    }
  });
}

document.addEventListener('DOMContentLoaded', () => {
  const analyzeBtn = document.getElementById('analyze-btn');
  const textInput = document.getElementById('text-input');
  const imageInput = document.getElementById('image-input');
  const urlInput = document.getElementById('url-input');
  const modelSelect = document.getElementById('model-select');

  analyzeBtn.addEventListener('click', () => {
    const text = textInput.value;
    const imageFile = imageInput.files[0];
    const url = urlInput.value;
    const model = modelSelect.value;

    if (text) {
      fetchAnalysis(text, url, model);
    } else if (imageFile) {
      const reader = new FileReader();
      reader.onload = (e) => {
        const imageData = e.target.result;
        fetchImageAnalysis(imageData, url, model);
      };
      reader.readAsDataURL(imageFile);
    } else {
      alert("Please enter text or select an image to analyze.");
    }
  });
});
