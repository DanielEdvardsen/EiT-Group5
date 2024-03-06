import MusicSelector from "@/app/ui/components/music-selector";
import Brain from "@/app/ui/components/brain";

export default function Home() {
    return (
        <main
            className="flex flex-row justify-center items-center min-h-screen p-24 space-x-4">
            <div className="w-1/2"> {/* Adjust the width as needed */}
                <Brain/>
            </div>
            <div className="w-1/2"> {/* Adjust the width as needed */}
                <MusicSelector/>
            </div>
        </main>
    );
}
