'use client'
import { useState, useEffect } from "react";
import { useRouter } from "next/navigation";
import Card from "@comps/card";
import ModalView from "@comps/modalView";
import ModalProfile from "@comps/modalProfile";
import { useAuth } from '@comps/authContext'

export default function Find() {
  const [token, updateToken] = useAuth();
  const [getCards, setCards] = useState([]);
  const [getModalData, setModalData] = useState([]);

  const router = useRouter();

  function checkLogin() {
    if (token === null && typeof token !== 'string') {
      router.push("/login/");
    }
  }

  // Busca as informações dos cards no back
  function getAllCards() {
    checkLogin()
    const url = "http://127.0.0.1:8000/profiles/all/";

    const data = {
      method: 'GET',
      headers: { Authorization: 'Token ' + token },
    };

    fetch(url, data)
      .then((res) => res.json())
      .then((data) => {
        createCards(data);
      });
  }

  function createCards(value) {
    if (value) {
      setCards(
        value.map((data, index) => (
          <Card key={index} name={data.name} lastname={data.lastname} id={data.id} area={data.area}
            profession={data.profession} picture={data.picture} favorite={data.favorite} 
            setModalData={setModalData} update={getAllCards}>
          </Card>
        ))
      );
    }
  }

  useEffect(() => {
    getAllCards()
  }, [])

  return (
    <>
      <div className='page'>
        <div className='align-cards'>
          {getCards}
        </div>
      </div>

    <ModalView data={getModalData}></ModalView>
    <ModalProfile update={getAllCards}></ModalProfile>
    </>
  )
}