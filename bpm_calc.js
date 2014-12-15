function init() {
  try {
    // Fix up for prefixing
    window.AudioContext = window.AudioContext||window.webkitAudioContext;
    context = new AudioContext();
    alert('We\'re good');
  }
  catch(e) {
    alert('Web Audio API is not supported in this browser');
  }
}

function loadSong(url) {
  var request = new XMLHttpRequest();
  request.open('GET', url, true);
  request.responseType = 'arraybuffer';

  // Decode asynchronously
  request.onload = function () {
      context.decodeAudioData(request.response, function (buffer) {
          console.log('Done loading song.');
          getTempo(buffer);
      }, function (err) { console.log('Error:', err); });
  }
  request.send();
}


window.addEventListener('load', init, false);
var songBuffer = null;
// Fix up prefixing
window.AudioContext = window.AudioContext || window.webkitAudioContext;

var context = new AudioContext();

var songUrl = 'http://localhost:8092/thunderstruck.mp3';

loadSong(songUrl);

function getTempo(buffer) {

    var queryInput = document.querySelector('#query'),
    result = document.querySelector('#result'),
    text = document.querySelector('#text'),
    audioTag = document.querySelector('#audio');

    //console.log(buffer);

        // Create offline context
        var offlineContext = new OfflineAudioContext(1, buffer.length, buffer.sampleRate);

        // Create buffer source
        var source = offlineContext.createBufferSource();
        source.buffer = buffer;

        // Create filter
        var filter = offlineContext.createBiquadFilter();
        filter.type = "lowpass";

        // Pipe the song into the filter, and the filter into the offline context
        source.connect(filter);
        filter.connect(offlineContext.destination);

        // Schedule the song to start playing at time:0
        source.start(0);

        // Render the song
        offlineContext.startRendering();

        // Act on the result
        offlineContext.oncomplete = function (e) {
            // Filtered buffer!
            var filteredBuffer = e.renderedBuffer;

            var peaks,
        initialThresold = 0.9,
        thresold = initialThresold,
        minThresold = 0.3,
        minPeaks = 30;

            do {
                peaks = getPeaksAtThreshold(e.renderedBuffer.getChannelData(0), thresold);
                thresold -= 0.05;
            } while (peaks.length < minPeaks && thresold >= minThresold);

            //var svg = document.querySelector('#svg');
            //svg.innerHTML = '';
            //peaks.forEach(function (peak) {
                //svg.innerHTML += '<rect x="' + (100 * peak / e.renderedBuffer.length) + '%" y="0" width="1" height="100%"></rect>';
            //});
            //svg.innerHTML += '<rect id="progress" y="0" width="1" height="100%"></rect>';

            var intervals = countIntervalsBetweenNearbyPeaks(peaks);

            var groups = groupNeighborsByTempo(intervals, filteredBuffer.sampleRate);

            var top = groups.sort(function (intA, intB) {
                return intB.count - intA.count;
            }).splice(0, 5);

            text.innerHTML = '<div id="guess">Guess for track <strong>' + songUrl + '</strong> is <strong>' + Math.round(top[0].tempo) + ' BPM</strong>' +
        ' with ' + top[0].count + ' samples.</div>';

            text.innerHTML += '<div class="small">Other options are ' +
        top.slice(1).map(function (group, index) {
            return group.tempo + ' BPM (' + group.count + ')';
        }).join(', ') +
        '</div>';
            result.style.display = 'block';
        };
}



var previewUrl = 'http://localhost:8092/thunderstruck.mp3';

var context = new AudioContext();
var request = new XMLHttpRequest();
request.open('GET', previewUrl, true);
request.responseType = 'arraybuffer';
request.onload = function () {
    context.decodeAudioData(request.response, function (buffer) {
        console.log(buffer);

        // Create offline context
        var offlineContext = new OfflineAudioContext(1, buffer.length, buffer.sampleRate);

        // Create buffer source
        var source = offlineContext.createBufferSource();
        source.buffer = buffer;

        // Create filter
        var filter = offlineContext.createBiquadFilter();
        filter.type = "lowpass";

        // Pipe the song into the filter, and the filter into the offline context
        source.connect(filter);
        filter.connect(offlineContext.destination);

        // Schedule the song to start playing at time:0
        source.start(0);

        // Render the song
        offlineContext.startRendering();

        // Act on the result
        offlineContext.oncomplete = function (e) {
            // Filtered buffer!
            var filteredBuffer = e.renderedBuffer;

            var peaks,
        initialThresold = 0.9,
        thresold = initialThresold,
        minThresold = 0.3,
        minPeaks = 30;

            do {
                peaks = getPeaksAtThreshold(e.renderedBuffer.getChannelData(0), thresold);
                thresold -= 0.05;
            } while (peaks.length < minPeaks && thresold >= minThresold);

            var svg = document.querySelector('#svg');
            svg.innerHTML = '';
            peaks.forEach(function (peak) {
                svg.innerHTML += '<rect x="' + (100 * peak / e.renderedBuffer.length) + '%" y="0" width="1" height="100%"></rect>';
            });
            svg.innerHTML += '<rect id="progress" y="0" width="1" height="100%"></rect>';

            var intervals = countIntervalsBetweenNearbyPeaks(peaks);

            var groups = groupNeighborsByTempo(intervals, filteredBuffer.sampleRate);

            var top = groups.sort(function (intA, intB) {
                return intB.count - intA.count;
            }).splice(0, 5);

            text.innerHTML = '<div id="guess">Guess for track <strong>' + previewUrl + '</strong> is <strong>' + Math.round(top[0].tempo) + ' BPM</strong>' +
        ' with ' + top[0].count + ' samples.</div>';

            text.innerHTML += '<div class="small">Other options are ' +
        top.slice(1).map(function (group, index) {
            return group.tempo + ' BPM (' + group.count + ')';
        }).join(', ') +
        '</div>';
            result.style.display = 'block';
        };
    }, function () { });
};

// Function to identify peaks
function getPeaksAtThreshold(data, threshold) {
  var peaksArray = [];
  var length = data.length;
  for(var i = 0; i < length;) {
    if (data[i] > threshold) {
      peaksArray.push(i);
      // Skip forward ~ 1/4s to get past this peak.
      i += 10000;
    }
    i++;
  }
  return peaksArray;
}

// Function used to return a histogram of peak intervals
function countIntervalsBetweenNearbyPeaks(peaks) {
  var intervalCounts = [];
  peaks.forEach(function(peak, index) {
    for(var i = 0; i < 10; i++) {
      var interval = peaks[index + i] - peak;
      var foundInterval = intervalCounts.some(function(intervalCount) {
        if (intervalCount.interval === interval)
          return intervalCount.count++;
      });
      if (!foundInterval) {
        intervalCounts.push({
          interval: interval,
          count: 1
        });
      }
    }
  });
  return intervalCounts;
}

// Function used to return a histogram of tempo candidates.
function groupNeighborsByTempo(intervalCounts, sampleRate) {
  var tempoCounts = [];
  intervalCounts.forEach(function(intervalCount, i) {
    if (intervalCount.interval !== 0) {
      // Convert an interval to tempo
      var theoreticalTempo = 60 / (intervalCount.interval / sampleRate );

      // Adjust the tempo to fit within the 90-180 BPM range
      while (theoreticalTempo < 90) theoreticalTempo *= 2;
      while (theoreticalTempo > 180) theoreticalTempo /= 2;

      theoreticalTempo = Math.round(theoreticalTempo);
      var foundTempo = tempoCounts.some(function(tempoCount) {
        if (tempoCount.tempo === theoreticalTempo)
          return tempoCount.count += intervalCount.count;
      });
      if (!foundTempo) {
        tempoCounts.push({
          tempo: theoreticalTempo,
          count: intervalCount.count
        });
      }
    }
  });
  return tempoCounts;
}