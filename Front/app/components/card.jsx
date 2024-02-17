import { faStar } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { useState } from "react";

export default function Card(props) {
  const [getToken, setToken] = useState(typeof window !== 'undefined' ? sessionStorage.getItem('token') : null);

  function showModal() {
    const modal = document.getElementById('modalView')
    modal.style.visibility = 'visible'
  }

  function receiveModalData() {
    const url = 'http://127.0.0.1:8000/profiles/all/'
    const form = new FormData()
    form.append('profileId', props.id)

    const data = {
      method: 'POST',
      headers: { Authorization: 'Token ' + getToken },
      body: form
    }

    fetch(url, data)
      .then((res) => res.json())
      .then((data) => {
        props.setModalData(data)
      })
      .then(() => {
        showModal()
      })
  }

  function changeFavorite(event) {
    event.stopPropagation()
    const url = 'http://127.0.0.1:8000/profiles/favorites/'
    const form = new FormData()
    form.append('profileId', props.id)

    const data = {
      method: 'POST',
      headers: { Authorization: 'Token ' + getToken },
      body: form
    }

    fetch(url, data)
    .then(() => {
      props.update()
    })
  }

  const FAVORITE = () => {
    const favClass = props.favorite ? 'is-fav' : 'not-fav'
    return (
      <div className="card-fav-icon">
        <FontAwesomeIcon icon={faStar} size="xl" className={favClass} onClick={changeFavorite}/>
      </div>
    ) 
  }

  return (
    <div className="card-margin">
      <div className="card" onClick={receiveModalData}>
        {FAVORITE()}
        <img src={props.picture} alt="" className="card-pic" />
        <span className="card-title">{props.profession}</span>
        <span className="card-name">{props.name} {props.lastname}</span>
        <span className="card-area">{props.area}</span>
        <span className="card-fav"> {props.favorite.toString()} </span>
      </div>
    </div>
  )
}