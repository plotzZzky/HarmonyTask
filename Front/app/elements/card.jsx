import { useState } from "react";

export default function Card(props) {
  const [getToken, setToken] = useState(typeof window !== 'undefined' ? sessionStorage.getItem('token') : null);
  const image = `http://127.0.0.1:8000${props.picture}`

  function showModal() {
    const modal = document.getElementById('modalView')
    modal.style.visibility = 'visible'
  }

  function receiveModalData() {
    const url = 'http://127.0.0.1:8000/profiles/'
    const form = new FormData()
    form.append('profileId', props.id)

    let data = {
      method: 'POST',
      headers: { Authorization: 'Token ' + getToken },
      body: form
    }

    fetch(url, data)
      .then((res) => res.json())
      .then((data) => {
        props.setModalData(data['profile'])
      })
      .then(() => {
        showModal()
      })
  }

  return (
    <div className="card-margin">
      <div className="card" onClick={receiveModalData}>
        <img src={image} alt="" className="card-pic" />
        <span className="card-title">{props.profession}</span>
        <span className="card-name">{props.name} {props.lastname}</span>
        <span className="card-profession">{props.profession}</span>
      </div>
    </div>
  )
}