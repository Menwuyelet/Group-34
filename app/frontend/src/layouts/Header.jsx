import React, { useState } from 'react';
import logo from '/public/images/logos/logo-white.png'
import search from '/public/icons/search_icon.png'
import ethio from '/public/icons/ethiopia.png'


function Header() {
    const [showModal, setShowModal] = useState(false);
    return (
        <>  
            {/*Container for the Header*/}
            <div className='flex bg-blue-900 py-3 px-10 items-center justify-between fixed top-0 right-0 left-0'>


                {/*The Logo and the name GuzoMate */}
                <div className=' '>
                    <a href="#"  
                        className='flex gap-2 font-bold text-white items-center w-[100px] justify-right text-[25px]'>
                        <img className='w-10' src={logo}></img> GuzoMate
                    </a>
                </div>


                {/*Search Icon, Language, Currency, (register and sign-up) */}
                <div className='flex justify-end items-center gap-5 mr-1'>~~
                    <img src={search}
                    className='w-7 h-7 cursor-pointer'></img>

                    <img  onClick={()=>setShowModal(true)} src={ethio} alt="" className='w-7 cursor-pointer'/>

                    <div className='flex items-center'>
                    <button className='flex items-center gap-1 bg-transparent text-[20px] rounded-[5px] text-white px-3 py-[2px] cursor-pointer font-bold hover:bg'>USD</button>
                    </div>
                <button className='flex items-center gap-1 bg-amber-500 text-[15px] rounded-[5px] text-white px-5 py-[10px] cursor-pointer font-bold hover:bg-amber-700'>Resigter</button>
                <button className='flex items-center gap-1 bg-amber-500 text-[15px] rounded-[5px] text-white px-5 py-[10px] cursor-pointer font-bold hover:bg-amber-700'>Sign in</button>
                </div>
            </div>




            {/*Popup for the register */}
                {showModal && (

                    <div onClick={()=>setShowModal(false)}className='fixed flex bg-black/50 min-h-screen w-screen z-1 items-center justify-center pb-[5%]'>
                        <div onClick={(e) => e.stopPropagation()} className='bg-white rounded-[10px] w-[350px] h-[500px] flex-cols justify-center pt-5'>

                            <h1 className='place-self-centers text-black-200 text-[40px]'>Sign in</h1>

                            <div className='p-10'>
                                <form action="">
                                    <input className='border-1 border-gray-600 rounded-[8px] w-full h-[40px] p-[10px] mb-[20px]' type="text" placeholder='Full Name'/>                          
                                    <input className='border-1 border-gray-600 rounded-[8px] w-full h-[40px] p-[10px] mb-[20px]'type="text" placeholder='Email' />
                                    <input className='border-1 border-gray-600 rounded-[8px] w-full h-[40px] p-[10px] mb-[20px]'type="password" placeholder='Password'/>
                                    <button className='bg-blue-600 text-white font-bold p-2 w-full h-[40px] rounded-[6px] hover:bg-blue-900'>Sign up</button>
                                </form>
                            </div>
                        </div>
                    </div>
                )}





        </>
)}

export default Header;