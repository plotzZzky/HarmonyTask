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
    return areas.map((data, index) => (
      <span className='categories' key={index} onClick={() =>selectCategorie(data.name)}> {data.icon} {data.name} </span>
    ))
  }

  function filterCards(event) {
    const value = event.target.value.toLowerCase()
    const cards = document.querySelectorAll(".card-margin");

    cards.forEach(item => {
      const profession = item.querySelector(".card-title").innerHTML.toLowerCase()
      item.style.display = profession.includes(value)? 'block' : 'none'
    });
  }

  function selectCategorie(value) {
    const cards = document.querySelectorAll('.card-margin');

    cards.forEach(item => {
      const area = item.querySelector(".card-area").innerHTML.toLowerCase()
      item.style.display = area === value.toLowerCase() ? 'block' : 'none'
    });
  }

  function showAllCards() {
    const cards = document.querySelectorAll('.card-margin');
    cards.forEach(item => {
      item.style.display = 'block'
    });
  }

  function showFavorites() {
    const cards = document.querySelectorAll('.card-margin');
    cards.forEach(item => {
      const fav = item.querySelector(".is-fav");
      
      item.style.display = fav? 'block' : 'none'  
    });
  }

  return(
    <nav className="app-bar">
      <div className="app-bar-align">
        <input type="text" className="app-filter" onChange={filterCards} placeholder="Buscar por profissão"></input>
        <div className="align-categories">
          <span className="categories" onClick={showFavorites}> <FontAwesomeIcon icon={faStar}/> Favoritos </span>
          {categories()}
          <span className="categories" onClick={showAllCards}> <FontAwesomeIcon icon={faBars}/> Todos </span>
        </div>
      </div>
    </nav>
  )
}