'use client';
import AudioPlayer from 'react-h5-audio-player';
import 'react-h5-audio-player/lib/styles.css';
import React from "react";
import {
    FormControl,
    FormControlLabel,
    FormLabel,
    Radio,
    RadioGroup
} from "@mui/material";
import {genres, fetchSongs} from "../../lib/data";

export default function MusicSelector() {
    const [selectedGenre, setSelectedGenre] = React.useState<string>('');
    const [songs, setSongs] = React.useState<string[]>();
    const [currentSong, setCurrentSong] = React.useState<string | undefined>("");

    /**
     * Handle change of genre.
     * @param value: value of the selected genre.
     */
    async function handleChange(value: string) {
        setSelectedGenre(value);
        if (value) {
            await fetchSongs(value).then((songs) => {
                setSongs(songs);
                setCurrentSong(songs ? songs[0] : undefined)
            });
        }
    }

    /**
     * Handle click on next button.
     */
    const handleClickNext = () => {
        const currentIndex = songs?.findIndex(song => song === currentSong);
        if (currentIndex !== undefined) {
            setCurrentSong(songs ? songs[(currentIndex + 1) % songs.length] : "")
        }
    };

    /**
     * Handle click on previous button.
     */
    const handleClickPrev = () => {
        const currentIndex = songs?.findIndex(song => song === currentSong);
        if (currentIndex !== undefined) {
            setCurrentSong(songs ? songs[(currentIndex - 1 + songs.length) % songs.length] : "")
        }
    };
    /**
     * Music player component.
     * See docs at: https://www.npmjs.com/package/react-h5-audio-player
     */
    const Player = () => (
        <AudioPlayer
            autoPlay
            src={currentSong}
            onPlay={() => console.log('Now playing' + currentSong)}
            className="w-full h-12 bg-gray-200 rounded"
            showSkipControls={true}
            onClickNext={handleClickNext}
            onClickPrevious={handleClickPrev}
        />
    );

    return (
        <main className="flex flex-col items-center justify-center space-y-4">
            <FormControl className={' w-64'}>
                <FormLabel
                    className={'text-lg text-center'}
                    id="demo-row-radio-buttons-group-label">Select
                    genre</FormLabel>
                <RadioGroup
                    row
                    aria-labelledby="demo-row-radio-buttons-group-label"
                    name="row-radio-buttons-group"
                    value={selectedGenre}
                    onChange={(event) => handleChange(event.target.value)}
                    className="grid grid-cols-2 gap-4" // Use grid to create a two-column layout
                >
                    {genres.map((genre, index) => (
                        <FormControlLabel
                            key={index}
                            value={genre}
                            control={<Radio/>}
                            label={genre}
                            className="col-span-1"
                        />
                    ))}
                </RadioGroup>

            </FormControl>
            <div className="w-full max-w-md">
                <h3 className="text-xl font-bold">Now
                    playing: {currentSong?.split('/').pop()}</h3>
            </div>
            <div className="w-full max-w-md">
                <Player/>
            </div>
        </main>
    )
}
