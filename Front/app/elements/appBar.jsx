'use client'
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome"
import { faCross, faScaleBalanced, faUtensils, faWrench, faUser, faBars, faStar, faLaptop } from "@fortawesome/free-solid-svg-icons"

export default function AppBar() {

  const areas = [
    {"name": "Alimentos", "icon": <FontAwesomeIcon icon={faUtensils}/>},
    {"name": "Consertos", "icon": <FontAwesomeIcon icon={faWrench}/>},
    {"name": "Jurídico", "icon": <FontAwesomeIcon icon={faScaleBalanced}/>},
    {"name": "Saúde", "icon": <FontAwesomeIcon icon={faCross}/>},
    {"name": "Tecnologia", "icon": <FontAwesomeIcon icon={faLaptop}/>},
    {"name": "Outros", "icon": <FontAwesomeIcon icon={faUser}/>},
  ]

  const categories = () => {
    return areas.map((data) => (
      <span className='categories' onClick={() =>selectCategorie(data.name)}> {data.icon} {data.name} </span>
    ))
  }

  function filterCards(event) {
    const value = event.target.value.toLowerCase()
    const cards = document.querySelectorAll(".card-margin");

    cards.forEach(item => {
      const profession = item.querySelector(".card-profession").innerHTML.toLowerCase()
      item.style.display = profession.includes(value)? 'block' : 'none'
    });
  }

  function selectCategorie(value) {
    const cards = document.querySelectorAll('.card-margin');

    cards.forEach(item => {
      const profession = item.querySelector(".card-profession").innerHTML.toLowerCase()
      item.style.display = profession === value? 'block' : 'none'
    });
  }

  function ShowAllCards() {
    const cards = document.querySelectorAll('.card-margin');
    cards.forEach(element => {
      element.style.display = 'block'
    });
  }

  return(
    <nav className="app-bar">
      <div className="app-bar-align">
        <input type="text" className="app-filter" onChange={filterCards} placeholder="Buscar por area"></input>
        <div className="align-categories">
          <span className="categories" onClick={ShowAllCards}> <FontAwesomeIcon icon={faStar}/> Favoritos </span>
          {categories()}
          <span className="categories" onClick={ShowAllCards}> <FontAwesomeIcon icon={faBars}/> Todos </span>
        </div>
      </div>
    </nav>
  )
}