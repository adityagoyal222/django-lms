console.log(lessonData); // Example: This will log an array of lesson data
var players = {}; // This object will store all of the YouTube players

// Function to initialize YouTube players
function initializeYouTubePlayers() {
    
    for (var i = 0; i < lessonData.length; i++) {
        var lesson = lessonData[i];
        players[lesson.id] = new YT.Player('player' + lesson.id, {
            height: lesson.height,
            width: lesson.width,
            videoId: lesson.videoId,
            events: {
                'onReady': onPlayerReady,
                'onStateChange': onPlayerStateChange
            }
        });
    }
}

// Initialize YouTube players when the API is ready
function onYouTubeIframeAPIReady() {
    initializeYouTubePlayers();
    console.log("Youtube API Ready");
    console.log(players);
}

// Function to update progress for a specific lesson's video
function updateLessonProgress(lessonId) {
    const player = players[lessonId];
    if (player) {
        const currentTime = player.getCurrentTime();
        const duration = player.getDuration();
        const percentage = (currentTime / duration) * 100;

        // Check if the percentage is 70% or 100% before making the request
        if (percentage === 70 || percentage === 100) {
            // Send an AJAX POST request to update the progress
            const csrfToken = document.querySelector('input[name=csrfmiddlewaretoken]').value;

            fetch('/resources/update_video_progress/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                    'X-CSRFToken': csrfToken,
                },
                body: `lesson_id=${lessonId}&progress=${percentage}`,
            })
                .then((response) => response.json())
                .then((data) => {
                    console.log(data.message); // Log the response message
                })
                .catch((error) => {
                    console.error('Error:', error);
                });
        }
    }
}

// Function to handle when a lesson's video player is ready
function onPlayerReady(event) {
    // event.target.playVideo();
    const lessonId = event.target.getVideoData().video_id;
    startProgressTracking(lessonId);
}

// Function to start progress tracking for a specific lesson's video
function startProgressTracking(lessonId) {
    const progressInterval = setInterval(() => {
        updateLessonProgress(lessonId);
    }, 10000); // Update progress every 10 seconds (adjust as needed)
}

function onPlayerStateChange(event) {
    if (event.data === YT.PlayerState.ENDED) {
        const lessonId = event.target.getVideoData().video_id;
        clearInterval(progressInterval); // Stop progress tracking when the video ends
        updateLessonProgress(lessonId); // Ensure progress is 100% when the video ends
    }
}