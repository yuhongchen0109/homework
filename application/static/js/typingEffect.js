// Displays the typing text effect for the job titles on the main page

// Get the typing text from the JSON file
fetch("/static/text/jobTitles.json")
    .then(response => response.json())
    .then(data => {
        // Create a new instance of Typed.js
        var typed = new Typed("#typing-text", {
            strings: data.text,
            typeSpeed: 50,  // Speed at which characters are typed
            startDelay: 1000,  // Delay before typing starts (in milliseconds)
            loop: true  // Whether or not to loop the typing animation
        });
    });
