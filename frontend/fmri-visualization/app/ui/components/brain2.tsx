"use client";
import {useEffect, useState} from 'react';

const images = [
    '/neuron_activation.jpg',
    '/monkey_sony_walkman.jpg',
];

export default function Brain2() {
    const [currentImageIndex, setCurrentImageIndex] = useState(0);

    useEffect(() => {
        const intervalId = setInterval(() => {
            setCurrentImageIndex((currentImageIndex) => (currentImageIndex + 1) % images.length);
        }, 3000); // Change image every 3000 milliseconds (3 seconds)

        return () => clearInterval(intervalId); // Clean up the interval on component unmount
    }, []);

    return (
        /* <div className="transition duration-5000 ease-in-out">
             <Image
                 placeholder={'blur'}
                 blurDataURL={images[currentImageIndex]}
                 src={images[currentImageIndex]}
                 width={800}
                 height={300}
                 alt={'Monkey sees banana, neuron activation in brain!'}
             />
         </div>*/
        <canvas
            id="bg">

        </canvas>
    );
}
