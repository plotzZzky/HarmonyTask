'use client'
import { useState, useEffect } from "react";
import { useRouter } from "next/navigation";
import Card from "@elements/card";
import ModalView from "@elements/modalView";
import ModalProfile from "@elements/modalProfile";

export default function Find() {
  const [getToken, setToken] = useState(typeof window !== 'undefined' ? sessionStorage.getItem('token') : null);
  const [getCards, setCards] = useState([]);
  const [getModalData, setModalData] = useState([])

  const router = useRouter();

  function checkLogin() {
    if (getToken === null && typeof getToken !== 'string') {
      router.push("/login/");
    }
  }

  // Busca as informações dos cards no back
  function getAllCarts() {
    checkLogin()
    const url = "http://127.0.0.1:8000/profiles/all/";

    const data = {
      method: 'GET',
      headers: { Authorization: 'Token ' + getToken },
    };

    fetch(url, data)
      .then((res) => res.json())
      .then((data) => {
        createCards(data['profiles']);
      });
  }

  function createCards(value) {
    if (value) {
      setCards(
        value.map((data, index) => (
          <Card key={index} name={data.name} lastname={data.lastname} id={data.id} 
            profession={data.profession} picture={data.picture} setModalData={setModalData}>
          </Card>
        ))
      );
    }
  }

  useEffect(() => {
    getAllCarts()
  }, [])

  return (
    <>
      <div className='page'>
        <div className='align-cards'>
          {getCards}
        </div>
      </div>

    <ModalView data={getModalData}></ModalView>
    <ModalProfile></ModalProfile>
    </>
  )
}