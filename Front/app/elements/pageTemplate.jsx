'use client'
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import { faGithub } from '@fortawesome/free-brands-svg-icons'

import '../globals.css'

export default function PageTemplate({ nav, page }) {

  function goToGitHub() { router.push("https://github.com/plotzzzky") }

  return(
    <>
      <header>
        <NavBar></NavBar>
        {nav}
      </header>

      <main>
        {page}
      </main>

      <footer>
        <p className="link" onClick={goToGitHub}>
          <FontAwesomeIcon icon={faGithub} />
          <a> GitHub </a>
        </p>
      </footer>
    </>
  )
}