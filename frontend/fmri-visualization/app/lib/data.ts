const genres = [
    'Blues', 'Jazz', 'Classical', 'Country', 'Disco', 'Hiphop', 'Metal', 'Pop', 'Reggae', 'Rock'
];


const fetchSongs = async (genre: string) => {
    try {
        return Array.from({length: 10}, (_, i) => `/genres_original/${genre}/${genre}.000${i < 10 ? '0' : ''}${i}.wav`);
    } catch (error) {
        console.error(`Error fetching songs: ${error}`);
    }
}


export {genres, fetchSongs};
