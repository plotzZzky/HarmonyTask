import { FontAwesomeIcon } from "@fortawesome/react-fontawesome"
import { faWhatsapp } from "@fortawesome/free-brands-svg-icons"
import { faPhone, faEnvelope } from "@fortawesome/free-solid-svg-icons"


export default function ModalView(props) {

  const image = `http://127.0.0.1:8000${props.data.picture}`

  function closeModal() {
    const modal = document.getElementById('modalView')
    modal.style.visibility = 'hidden'
  }

  return (
    <div className="modal-background" id="modalView" onClick={closeModal}>
      <div className="modal" onClick={e => e.stopPropagation()}>
        <img src={image} alt="" className="modal-picture" />
        <span href="" className="modal-profession"> {props.data.profession} </span>
        <span href="" className="modal-name"> {props.data.name} {props.data.lastname} </span>

        <div className="modal-align-btns">
          <button className="modal-btn"> <FontAwesomeIcon icon={faWhatsapp}/> {props.data.telephone} </button>
          <button className="modal-btn"> <FontAwesomeIcon icon={faPhone} /> {props.data.telephone} </button>
          <button className="modal-btn"> <FontAwesomeIcon icon={faEnvelope} /> {props.data.email} </button>
        </div>

        <textarea value={props.data.description} readOnly='true'></textarea>

      </div>
    </div>
  )
}