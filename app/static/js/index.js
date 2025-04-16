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
  const response = await fetch(`https://spotify23.p.rapidapi.com/tracks/?ids=${encodeURIComponent(query)}`,options);
  const data = await response.json();
  const resultsList = document.getElementById('results');
  // resultsList.innerHTML = '';
  console.log(data)
  // data.results.forEach(song => {
  //   const listItem = document.createElement('li');
  //   listItem.textContent = `${song.trackName} by ${song.artistName}`;
  //   resultsList.appendChild(listItem);
  // });
});