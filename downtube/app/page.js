"use client"

import Image from 'next/image'
import { useState, useEffect } from 'react'
import useDownloader from 'react-use-downloader';

export default function Home() {
  const { size, elapsed, percentage, download, cancel, error, isInProgress } = useDownloader();
  
  const [link, setLink] = useState('');
  const [choice, setChoice] = useState('1');
  const [successMessage, setSuccessMessage] = useState('');
  const [title,setTitle] = useState('');
  const [fileurl,setFileUrl] = useState('')

  useEffect(() => {
    // Perform actions after 'title' state is updated
    if (title) {
      // Use ngrok URL and append the local file path
      setFileUrl(`https://randomstring.ngrok.io/gaane/${title}`);
    }
  }, [title]);
  

  const handleSubmit = async () => {
    try {
      const response = await fetch('http://127.0.0.1:5000/download', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ link, choice }),
      });

      if (response.ok) {
        const result = await response.json();
        setSuccessMessage(result.message);
        setTitle(result.title + ".mp4")
      } else {
        const error = await response.json();
        alert(`Error: ${error.message}`);
      }
    } catch (error) {
      console.error('Error:', error);
      alert('An error occurred. Please try again.');
    }
  };

  
  return (
    <div className='flex flex-col justify-center items-center h-screen p-4'>
     

     <h1 className=' text-5xl md:text-7xl font-semibold '> ▶️DownTube </h1>
     <div id='linkline1' className='flex flex-col md:flex-row gap-5 mt-5'>
    <h2 className='text-4xl'> Enter YouTube Link: </h2>
     <input value={link} onChange={(e)=> setLink(e.target.value)} className='border-2 border-black ' /> 
     </div>

    <div id='mp3mp4' className='flex mt-4 gap-4'>

    <h1 className='md:text-4xl text-2xl'>Choose MP3(Audio) or MP4(Video) : </h1>
    <select
          className='border-2 border-black p-2 rounded-2xl'
          value={choice}
          onChange={(e) => setChoice(e.target.value)}
        >
          <option  value='1'>MP3</option>
          <option  value='2'>MP4</option>
        </select>
    </div>
    <button onClick={handleSubmit} className='bg-[#00A6ED] p-4 rounded-2xl text-white text-4xl hover:scale-110 transition-all mt-5'> Submit </button>
    
    {successMessage && (
        <div className='mt-5 flex flex-col'>
          <p className='text-2xl'>{successMessage} </p>
          <a href={fileurl} download={title}>
          <div

            className='bg-[#00A6ED] p-4 rounded-2xl flex items-center justify-center text-white text-4xl hover:scale-110 transition-all mt-5'
          >Download
          </div>
            </a>
        </div>
      )}

      </div>
   
  )
}
