import { useState } from 'react'


function App() {

  const  [values, setValues] = useState({
    firstName: '',
    lastName: '',
    Address: '',
    StreetAddress: '',
    StreetAddress2: '',
    City: '',
    PostalZipCode: '',
    PhoneNumber: '',
    Email: '',
    ArrivalDateTime: '',
    DepartureDateTime: '',
    NumberOfAdults: 1,
    NumberOfChildren: 0,
    paymentMethod: '',
    Request: ''
  });

  const Radio = (e) => {
    setValues({...values, paymentMethod: e.target.value});
  }
  

  const handlechange = (e) => {
    setValues({...values, [e.target.name]: e.target.value});
  }

  const handlesubmit = (e) => {
    e.preventDefault();
    console.log(values);
    e.target.reset(); // Reset the form
  }

  return (
    < div className="">
     <div className="">

          {/* images container */}
          <img className='top-0 w-full h-100' src='./public/Addis Ababa.jpg' alt="Addis Ababa" />

          <div className='grid grid-cols-3 top-70 place-self-center gap-10 p-10 bg-white-300 absolute top-0'>
            
              <div className='relative bg-gray-500 w-60 h-40 border-5 border-solid border-white rounded-[20px] align-center justify-items-center p-5'> 
                <img className="w-20 h-20" src="guest.png" alt="screen" />
                <h3 className="text-white font-bold text-[20px]">Simple and quick</h3>
              </div>

              <div className='relative bg-gray-500 w-60 h-40 border-5 border-solid border-white rounded-[20px] align-center justify-items-center p-5'> 
                <img className="w-20 h-20" src="Booking.png" alt="screen" />
                <h3 className="text-white font-bold text-[20px]">Simple and quick</h3>
              </div>

              <div className='relative bg-gray-500 w-60 h-40 border-5 border-solid border-white rounded-[20px] align-center justify-items-center p-5'> 
                <img className="w-20 h-20" src="screen.png" alt="screen" />
                <h3 className="text-white font-bold text-[20px]">Simple and quick</h3>
              </div>

          </div>




            {/* text container */}
            <div className="relative mt-40 w-full h-40">
                <h1 className='font-black text-[35px] text-center '>Hotel Reservation Form</h1>
                <p className='text-center text-[20px] '>Please complete the form below</p>
            </div>

            <p className='text-[20px] relative text-center '>Your registration will be verified prior to your arrival</p>    
          








          {/* form container */}
          <div className="mt-5 p-10 w-full h-auto bg-white-300 justify-items-center place-self-center">
            <form onSubmit={handlesubmit}> 
              <div className="w-150 bg-white-300 place-self-center">

                {/* name section */}
                <label className="font-bold" htmlFor="Name">Name</label>
                <div className="grid grid-cols-2 gap-x-4 mb-10 w-full">
                  <input className="border-[1.5px] border-solid border-black-200 rounded-[6px] mb-3 mt-5 h-8" type="text" name='firstName'
                   onChange={(e)=>handlechange(e)} required/>
                  <input className="border-[1.5px]  border-solid border-black-200 rounded-[6px] mb-3 mt-5 h-8" type="text"   name="lastName"
                  onChange={(e)=>handlechange(e)} required/>
                  <p className="text-gray-500">First Name</p>
                  <p className="text-gray-500">Second Name</p>
                </div>

                
                {/* address section */}
                <label className="font-bold" htmlFor="Address">Address</label>
                <div className="grid grid-cols-1 gap-2 mt-5 mb-10 w-full">
                  <input className="border-[1.5px] border-solid border-black-200 rounded-[6px] h-8"type="text" name="Address" 
                  onChange={(e)=>handlechange(e)} required/>
                  <p className="text-gray-500">Street Address</p>
                  <input className="border-[1.5px] border-solid border-black-200 rounded-[6px] mt-5 h-8" type="text" name="StreetAddress" 
                   onChange={(e)=>handlechange(e)} required/>
                  <p className="text-gray-500">Street Address line 2</p>

                  <div className="grid grid-cols-2 gap-2 gap-x-4 w-full">
                    <input className="border-[1.5px] border-solid border-black-200 rounded-[6px] mt-5 h-8" type="text" name="StreetAddress2" 
                    onChange={(e)=>handlechange(e)} required/>
                    <input className="border-[1.5px] border-solid border-black-200 rounded-[6px] mt-5 h-8"type="text" name="City"
                     onChange={(e)=>handlechange(e)} required/>
                    <p className="text-gray-500">State/Province</p>
                    <p className="text-gray-500">City</p>
                  </div>
                  
                  <input className="border-[1.5px] border-solid border-black-200 rounded-[6px] mt-5 h-8" type="text"  name="PostalZipCode"
                   onChange={(e)=>handlechange(e)} required/>
                  <p className="text-gray-500">Postal / Zip Code</p>
                </div>


                {/* contact section */}
                <div className="grid grid-cols-2 gap-x-4 mb-15">
                  <label className="font-bold" htmlFor="contact">phone number</label>
                  <label className="font-bold" htmlFor="Email">Email</label>
                  <input className="border-[1.5px] border-solid border-black-200 rounded-[6px] mt-5 h-8" type="text" name="PhoneNumber"
                   onChange={(e)=>handlechange(e)} required/>
                  <input className="border-[1.5px] border-solid border-black-200 rounded-[6px] mt-5 h-8" type="text"  name="Email"
                   onChange={(e)=>handlechange(e)} required/>
                </div>


                {/* departure section */}
                <label className="font-bold" htmlFor="date">Arrival - Date and Time</label>
                <div className="grid grid-rows-2 gap-1 mt-5">
          
                  <div className="grid grid-rows-1 gap-1 mb-5">
                    <input className='border-[1.5px] border-solid border-black-200 rounded-[6px] p-2' type="datetime-local" name="ArrivalDateTime" 
                    onChange={(e)=>handlechange(e)} required/>       
                    <label className="text-gray-500" htmlFor="date">Date and Time</label>           
                  </div>

                  <div className="grid grid-rows-1 gap-1 mb-5">
                    <input className='border-[1.5px] border-solid border-black-200 rounded-[6px] p-2' type="datetime-local" name="DepartureDateTime" 
                    onChange={(e)=>handlechange(e)} required/>  
                    <label className="text-gray-500" htmlFor="date">Date and Time</label>                
                  </div>

                </div>



                <div className="grid grid-cols-2 gap-3 gap-x-4 mt-10 mb-10">
                  <label className="font-bold" htmlFor="Adults">Number of Adults</label>
                  <label className="font-bold" htmlFor="Children">Number of Children (if there are any)</label>
                  <input className="border-[1.5px] border-solid border-black rounded-[6px] p-2" type="number"  name="NumberOfAdults" min="1" max="100" defaultValue={1} 
                  onChange={(e)=>handlechange(e)} />
                  <input className="border-[1.5px] border-solid border-black rounded-[6px] p-2" type="number"  name="NumberOfChildren" min="0" max="100" defaultValue={0}
                  onChange={(e)=>handlechange(e)} required/>
                </div>
                
                <h3 className="font-bold">Payment Method</h3>

                  <div className="grid grid-cols-4">

                        <div className="mt-5">
                        <input type="radio" name='payment' value="check" id='check'
                        onChange={(e)=>Radio(e)} />
                        <label className="relative left-4" htmlFor="check">Check</label>
                        </div>

                        <label>
                          <input className="mt-5" type="radio" name='payment' value="visa" id='visa.png'
                          onChange={(e)=>Radio(e)} />
                            <img className="h-10 relative bottom-6 left-5" src="visa.png" alt="" />
                        </label>

                        <label>
                          <input className="mt-5" type="radio" name='payment' value="Commercial Bank of Ethiopia" id='CBE'
                          onChange={(e)=>Radio(e)}/>
                          <img className="h-10 relative bottom-8 left-5" src="CBE.png" alt="" />
                        </label>

                        <label>
                          <input className="mt-5" type="radio" name='payment' value="Apple"
                          onChange={(e)=>Radio(e)} />
                          <img className="h-10 relative bottom-7 left-8"  src="Apple.png" alt="" />
                        </label>

                        <label>
                          <input className="mt-5" type="radio" name='payment' value="Paypal"
                          onChange={(e)=>Radio(e)} />
                          <img className="h-10 relative bottom-6 left-6" src="Paypal.png" alt="paypal" />
                        </label>

                        <label>
                           <input className="mt-5" type="radio" name='payment' value="Telebirr" id='Telebirr'
                           onChange={(e)=>Radio(e)} />
                          <img className="h-10 relative bottom-8 left-6"  src="Telebirr.png" alt="" />
                        </label>

                        <label>
                          <input className="mt-5" type="radio" name='payment' value="mastercard" id='mastercard'
                           onChange={(e)=>Radio(e)} />
                          <img className="w-auto h-10 relative bottom-7 left-6" src="./public/Mastercard-logo.svg" alt="" />
                        </label>


                  </div>

                <div>
                  <h3 className='font-bold'>Do you have any special request</h3>
                  <input className='border border-solid border-black pb-20 pr-20 block mb-5 mt-2 rounded-[5px]' type="comment" placeholder='Type here...' name='Request'
                   onChange={(e)=>handlechange(e)} required/>
                  <button className='py-1 px-6 pt-2 pb-2 border border-solid border-none bg-[#bd6717] text-white cursor-pointer rounded-[5px]'>Submit</button>
                </div>
              </div>
            </form>
          </div>

           
     </div>
    </div>
  );
};

export default App