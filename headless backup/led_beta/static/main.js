document.addEventListener("DOMContentLoaded", () => {
  const brightnessSlider = document.getElementById("brightness-slider");
  const brightnessValue = document.getElementById("brightness-value");
  const blockSizeSlider = document.getElementById("block-size-slider");
  const blockSizeValue = document.getElementById("block-size-value");
  const blinkWaitSlider = document.getElementById("blink-wait-slider");
  const blinkWaitValue = document.getElementById("blink-wait-value");
  const slideWaitSlider = document.getElementById("slide-wait-slider");
  const slideWaitValue = document.getElementById("slide-wait-value");
  const buzzerWaitSlider = document.getElementById("buzzer-wait-slider");
  const buzzerWaitValue = document.getElementById("buzzer-wait-value");
  const colorButton = document.getElementById("color-button");
  const animationTypeRadios = document.getElementsByName("animation-type");
  const startButton = document.getElementById("start-button");
  const buzzerToggle = document.getElementById("buzzer-toggle");
  const counterValueElement = document.getElementById("counter-value");
  const focusButton = document.getElementById("focus-button");

  // Function to fetch the counter value from the server and update it in the frontend
  function updateCounter() {
    fetch("/api/get_counter")
      .then((response) => response.json())
      .then((data) => {
        counterValueElement.textContent = data.counter;
      })
      .catch((error) => console.error(error));
  }

  // Function to increment the counter in the frontend
  function incrementCounter() {
    const currentCounterValue = parseInt(counterValueElement.textContent);
    counterValueElement.textContent = currentCounterValue + 1;
  }

  // Function to reset the counter on the server and in the frontend
  function resetCounter() {
    fetch("/api/reset_counter", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ counter: 0 }),
    })
      .then((response) => response.json())
      .then((data) => {
        console.log(data);
        counterValueElement.textContent = 0;
      })
      .catch((error) => console.error(error));
  }

  // Update params on slider/input change
  brightnessSlider.addEventListener("input", () => {
    brightnessValue.textContent = brightnessSlider.value;
    updateParams({ brightness: parseFloat(brightnessSlider.value) });
  });

  blockSizeSlider.addEventListener("input", () => {
    blockSizeValue.textContent = blockSizeSlider.value;
    updateParams({ block_size: parseInt(blockSizeSlider.value) });
  });

  blinkWaitSlider.addEventListener("input", () => {
    blinkWaitValue.textContent = blinkWaitSlider.value;
    updateParams({ blink_wait: parseFloat(blinkWaitSlider.value) });
  });

  slideWaitSlider.addEventListener("input", () => {
    slideWaitValue.textContent = slideWaitSlider.value;
    updateParams({ slide_wait: parseFloat(slideWaitSlider.value) });
  });

  buzzerWaitSlider.addEventListener("input", () => {
    buzzerWaitValue.textContent = buzzerWaitSlider.value;
    updateParams({ buzzer_wait: parseFloat(buzzerWaitSlider.value) });
  });

  colorButton.addEventListener("input", () => {
    updateParams({ color: colorButton.value });
  });

  animationTypeRadios.forEach((radio) => {
    radio.addEventListener("change", () => {
      updateParams({ selected_animation: radio.value });
    });
  });
  
  // Focus button click event handler
  focusButton.addEventListener("click", () => {
    fetch("/api/focus_animation", {
        method: "POST",
    })
    .then((response) => response.json())
    .then((data) => {
        console.log("Focus animation triggered:", data);
    })
    .catch((error) => {
        console.error("Error triggering focus animation:", error);
    });
  });

  // Start/stop animation
  startButton.addEventListener("click", () => {
    const animationRunning = startButton.classList.contains("active");
    if (animationRunning) {
      stopAnimation();
      clearInterval(intervalId); // Clear the interval when animation is stopped
    } else {
      startAnimation();
      updateCounter(); // Call updateCounter immediately when animation starts
      intervalId = setInterval(updateCounter, 300); // Store the interval ID
    }
  });

  // Use Buzzer toggle
  buzzerToggle.addEventListener("change", () => {
    updateParams({ use_buzzer: buzzerToggle.checked });
  });

  // Update params via API
  function updateParams(newParams) {
    fetch("/api/update_params", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(newParams),
    })
      .then((response) => response.json())
      .then((data) => console.log(data))
      .catch((error) => console.error(error));
  }

  // Start animation via API
  function startAnimation() {
    fetch("/api/start_animation", { method: "POST" })
      .then((response) => response.json())
      .then((data) => {
        console.log(data);
        startButton.classList.add("active");
        startButton.textContent = "Stop";
      })
      .catch((error) => console.error(error));
  }

  // Stop animation via API
  function stopAnimation() {
    fetch("/api/stop_animation", { method: "POST" })
      .then((response) => response.json())
      .then((data) => {
        console.log(data);
        startButton.classList.remove("active");
        startButton.textContent = "Start";

        // Reset the counter value on the webpage to 0 after stopping the animation
        resetCounter();
      })
      .catch((error) => console.error(error));
  }

});