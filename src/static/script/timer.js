
;(function () {

  // Opt into strict mode
  'use strict';


  //
  // Variables
  //

  // The timer duration
  const duration = 1500;

  // The timer component
  let app;

  // The timer interval
  let timer;


  //
  // Functions
  //

  /**
   * Class representing a state-based component
   */
  class Rue {
    /**
     * Create a new state-based component
     * @param {String} selector A CSS selector for the target element
     * @param {Object} options The data and template for the component
     * @returns {Rue} The new state-based component
     */
    constructor (selector, options) {
      this.elem = document.querySelector(selector);
      this.data = options.data;
      this.template = options.template;
    }

    /**
     * Render the component
     */
    render () {
      this.elem.innerHTML = this.template(this.data);
    }
  }

  /**
   * Get the initial data for the timer
   * @returns {Object} The initial timer data
   */
  function getData () {
    return {
      time: duration,
      paused: true
    };
  }

  /**
   * Format the time into M:SS
   * @param {Number} time The time remaining
   * @returns {String} The time in M:SS format
   */
  function format (time) {
    // Get the minutes and seconds
    const minutes = Math.floor(time / 60).toString();
    const seconds = (time % 60).toString();

    // Return the time in M:SS format
    return minutes + ':' + seconds.padStart(2, '0');
  }

  /**
   * Get the template for the timer
   * @param {Object} props The data for the timer
   * @returns {String} An HTML string
   */
  function template (props) {
    // Get the paused state
    const pausedState = props.paused ? 'Start' : 'Pause';

    // If the timer is done, show a reset button
    if (props.time < 1) {
      return `
        <p>
          Times up!
        </p>
        <p>
          <button id="reset" type="button">
            Reset
          </button>
        </p>
      `;
    }

    // Otherwise, show the time remaining
    return `
      <p>
        ${format(props.time)}
      </p>
      <p>
        <button id="${pausedState.toLowerCase()}" type="button">
          ${pausedState}
        </button>
        <button id="reset" type="button">
          Reset
        </button>
      </p>
    `;
  }

  /**
   * Update the timer
   */
  function countdown () {
    // Decrease the time remaining
    app.data.time--;

    // If the timer is done, stop it
    if (app.data.time < 1) {
      clearInterval(timer);
    }

    // Render the new state
    app.render();
  }

  /**
   * Start the timer
   */
  function start () {
    // Set the paused state
    app.data.paused = false;

    // Re-render the timer
    app.render();

    // Start the countdown
    timer = setInterval(countdown, 1000);
  }

  /**
   * Pause the timer
   */
  function pause () {
    // Set the paused state
    app.data.paused = true;

    // Re-render the timer
    app.render();

    // Stop the countdown
    clearInterval(timer);
  }

  /**
   * Reset the timer
   */
  function reset () {
    // Reset the state
    app.data = getData();

    // Re-render the timer
    app.render();

    // Stop the countdown
    clearInterval(timer);
  }

  /**
   * Handle click events
   * @param {Event} event The Event interface
   */
  function handleClick (event) {
    switch (event.target.id) {
      case 'start':
        start();
        break;
      case 'pause':
        pause();
        break;
      case 'reset':
        reset();
    }
  }


  //
  // Inits & Event Listeners
  //

  // Set up the timer component
  app = new Rue('#app', {
    data: getData(),
    template: template
  });

  // Run an initial render
  app.render();

  // Handle click events
  app.elem.addEventListener('click', handleClick);

})();