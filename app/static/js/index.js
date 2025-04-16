document.getElementById('searchForm').addEventListener('submit', async function(e) {
  e.preventDefault();
  const query = document.getElementById('searchInput').value;
  const options = {
    method: 'GET',
    headers: {
      'x-rapidapi-host': 'spotify23.p.rapidapi.com',
      'x-rapidapi-key':'d60c0ceb86mshc7679ee4bdfb2afp159344jsn8dadcbcf9ac5'
    }
  };
  try {
  const response = await fetch(`https://spotify23.p.rapidapi.com/tracks/?ids=${encodeURIComponent(query)}`,options);
  if (!response.ok) {
    throw new Error(`HTTP error! Status: ${response.status}`);
  }
  const data = await response.json();
  console.log(data);
  console.log(data.tracks[0]);
  const trackInfo = {
    "Track Name" : data.tracks[0].name,
    Artists : data.tracks[0].artists.map(artist=> artist.name),
    "Popularity" : data.tracks[0].popularity,
    "Duration in MS" : data.tracks[0].duration_ms,
    "Album Name" : data.tracks[0].album.name,
    "Album Type" : data.tracks[0].album.album_type,
    "Album Release Date" : data.tracks[0].album.release_date,
    "Total Tracks" : data.tracks[0].album.total_tracks,
  };

  const trackImage = data.tracks[0].album.images[0].url;
  
  const result = document.getElementById('result');
  const resultImage = document.getElementById('resultImage');
  const resultInfo = document.getElementById('resultInfo');
  result.classList.remove("hidden");
  resultImage.src = trackImage;
  resultInfo.innerHTML = '';
  for (const [key, value] of Object.entries(trackInfo)) {
    const p = document.createElement('p');
    p.textContent = `${key}: ${Array.isArray(value) ? value.join(', ') : value}`;
    resultInfo.appendChild(p);
  }
} catch (error) {
    console.error('Error fetching data:', error);
  }

});