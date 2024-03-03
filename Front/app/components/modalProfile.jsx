import { useState, useEffect } from "react";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome"
import { faUtensils, faWrench, faScaleBalanced, faCross, faLaptop, faUser } from "@fortawesome/free-solid-svg-icons"

export default function ModalProfile(props) {
  const [getToken, setToken] = useState(typeof window !== 'undefined' ? sessionStorage.getItem('token') : null);

  const [getName, setName] = useState("");
  const [getLastName, setLastName] = useState("");
  const [getTelephone, setTelephone] = useState("");
  const [getDesc, setDesc] = useState("");
  const [getArea, setArea] = useState("");
  const [getProfession, setProfission] = useState("");
  const [getActive, setActive] = useState(true);

  const [getImageUser, setImageUser] = useState();
  const [getFileUser, setFileUser] = useState();

  const areas = [
    {"name": "Alimentos", "icon": <FontAwesomeIcon icon={faUtensils}/>},
    {"name": "Consertos", "icon": <FontAwesomeIcon icon={faWrench}/>},
    {"name": "Jurídico", "icon": <FontAwesomeIcon icon={faScaleBalanced}/>},
    {"name": "Saúde", "icon": <FontAwesomeIcon icon={faCross}/>},
    {"name": "Tecnologia", "icon": <FontAwesomeIcon icon={faLaptop}/>},
    {"name": "Outros", "icon": <FontAwesomeIcon icon={faUser}/>},
  ]

  function closeModal() {
    const modal = document.getElementById('modalProfile')
    modal.style.visibility = 'hidden'
  }

  function clickInput() {
    const input = document.getElementById('selectImgUser')
    input.click()
  }

  function changeImage(event) {
    const file = event.target.files[0];
    setImageUser(file)
    const reader = new FileReader();

    reader.onload = function (event) {
      setFileUser(event.target.result)
    };
    reader.readAsDataURL(file);
  }

  // Recebe os dados do perfil profissional do back
  function receiveModalData() {
    const url = 'http://127.0.0.1:8000/profiles/your/';
  
    const data = {
      method: 'GET',
      headers: { Authorization: 'Token ' + getToken },
    };
  
    fetch(url, data)
      .then((res) => {
        if (res.status === 200) {
          return res.json();
        } else {
          throw new Error(`Erro na solicitação com status ${res.status}`);
        }
      })
      .then((data) => {
        fillOutForm(data);
      })
      .catch((error) => {
        console.error(error.message);
      });
  }
  
  // Preenche os useStates e o forms
  function fillOutForm(data) {
    if (data) {
      setName(data.name)
      setLastName(data.lastname)
      setTelephone(data.telephone)
      setArea(data.area)
      setProfission(data.profession)
      setDesc(data.description)
      setFileUser(data.picture)
      setActive(data.active)
    }
  }

  function validateForm() {
    if (getImageUser, getFileUser, getName, getLastName, getTelephone, getArea, getProfession, getDesc) {
      createProfile()
    } else {
      alert("Preencha o formulario corretamente!")
    }
  }

  function createProfile() {
    const url = 'http://127.0.0.1:8000/profiles/your/';
    const form = new FormData();

    form.set('enctype', 'multipart/form-data');
    form.append("name", getName);
    form.append("lastName", getLastName);
    form.append("telephone", getTelephone);
    form.append("description", getDesc);
    form.append("area", getArea);
    form.append("profession", getProfession);
    form.append("active", getActive)
    if (getImageUser) {
      form.append('image', getImageUser, getImageUser.name);
    }

    const formData = {
      method: 'POST',
      headers: {
        Authorization: 'Token ' + getToken,
      },
      body: form,
    };
  
    fetch(url, formData)
      .then((res) => res.json())
      .then((data) => {
        fillOutForm(data);
      })
      .catch((error) => {
        console.error('Erro ao enviar formulário:', error);
      });

    props.update()
    closeModal();
  }

  function updateName(event) {
    const value = event.target.value;
    setName(value)
  }

  function updateLastName(event) {
    const value = event.target.value;
    setLastName(value)
  }

  function updateTelephone(event) {
    const value = event.target.value;
    setTelephone(value)
  }

  function updateDesc(event) {
    const value = event.target.value;
    setDesc(value)
  }

  function updateProfission(event) {
    const value = event.target.value;
    setProfission(value)
  }

  function updateArea() {
    const value = document.getElementById("selectArea").value
    setArea(value)
  }

  function updateActive() {
    const value = document.getElementById("selectActive").value
    setActive(value)
  }

  useEffect(() => {
    receiveModalData()
  }, [])

  return (
    <div className="modal-background" id="modalProfile" onClick={closeModal}>
      <div className="modal" onClick={e => e.stopPropagation()}>
        <h2> Seu perfil profissional </h2>
        <div className="align-inputs">
          <div className="align-imgs">
            <img className='preview-img' onClick={clickInput} src={getFileUser}></img>
            <input type="file" className="select-image" id='selectImgUser' onChange={changeImage}></input>
          </div>

          <input type="text" className="text-input" placeholder="Seu nome" value={getName} onChange={updateName}/>
          <input type="text" className="text-input" placeholder="Seu Sobrenome" value={getLastName} onChange={updateLastName}/>
          <input type="text" className="text-input" placeholder="Seu Telefone para contato" value={getTelephone} onChange={updateTelephone}/>

          <select id="selectArea" value={getArea} onChange={updateArea}>
            {areas.map((data, index) => (
              <option key={index}> {data.name} </option>
            ))}
          </select>

          <input type="text" className="text-input" placeholder="Sua profissão" value={getProfession} onChange={updateProfission}/>
          <textarea placeholder="Descreva seu trabalho.." style={{background: 'snow'}} value={getDesc} onChange={updateDesc}></textarea>

          <select id="selectActive" onChange={updateActive}>
            <option value={true}> Perfil ativo </option>
            <option value={false}> Perfile Inativo </option>
          </select>

          <button className="modal-btn" onClick={validateForm}> Salvar </button>
        </div>
      </div>
    </div>
  )
}