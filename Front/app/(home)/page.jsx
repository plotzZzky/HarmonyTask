'use client'
import { useState } from 'react';
import { useRouter } from 'next/navigation';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import { faSuitcase } from '@fortawesome/free-solid-svg-icons';

export default function Home() {
  const [getToken, setToken] = useState(typeof window !== 'undefined' ? sessionStorage.getItem('token') : null);
  const router = useRouter();

  const ABOUT = `Bem-vindo à HarmonyTask Network, o seu destino confiável para conectar-se a profissionais qualificados e prestadores de serviços em diversas áreas. 
  Nossa missão é criar uma plataforma harmoniosa onde clientes e prestadores de serviços possam se encontrar, colaborar e alcançar seus objetivos com facilidade e confiança.`

  const FAQ = [
    {
      question: "A HarmonyTask Network é totalmente gratuita?",
      answer: "Sim, a HarmonyTask Network é uma plataforma totalmente gratuita. Todos os recursos essenciais estão disponíveis para os usuários sem custos associados."
    },
    {
      question: "Quais são os serviços oferecidos pela HarmonyTask Network?",
      answer: "A HarmonyTask Network inclui acesso a uma ampla variedade de profissionais e prestadores de serviços. Você pode explorar, contratar e aproveitar os recursos essenciais sem nenhum custo."
    },
    {
      question: "Como faço para obter suporte técnico na HarmonyTask Network?",
      answer: "Para obter suporte técnico na HarmonyTask Network, visite nossa seção de Suporte em nosso site. Nossa equipe está pronta para ajudar a resolver qualquer dúvida ou problema que você possa ter."
    },
    {
      question: "Posso oferecer meus serviços na HarmonyTask Network de forma gratuita?",
      answer: "Sim, profissionais e prestadores de serviços podem se cadastrar e oferecer seus serviços gratuitamente na HarmonyTask Network. A plataforma é uma comunidade colaborativa onde todos têm a oportunidade de participar."
    },
    {
      question: "Como a HarmonyTask Network garante a qualidade dos profissionais cadastrados?",
      answer: "A HarmonyTask Network realiza verificações detalhadas para garantir a qualidade e confiabilidade dos profissionais cadastrados. Nossa prioridade é fornecer aos usuários acesso a serviços de alta qualidade."
    },
  ];


  const BENEFITS = [
    {"topic": "Variedade de Serviços:", 
    "answer": '- Conectamos clientes a uma ampla gama de profissionais, desde especialistas em TI até prestadores de serviços domésticos.'},

    {"topic": "Facilidade de Uso:", 
    "answer": '- Navegação simples e intuitiva para encontrar, avaliar e contatar profissionais em um único lugar.'},

    {"topic": "Compromisso com a Qualidade:",
     "answer": '-  Cada profissional em nossa plataforma é selecionado para proporcionar uma experiência excepcional.'}
  ]

  // Cria os items do faq
  const faqItems = () => {
    return FAQ.map((data, index) => (
      <details key={index}>
        <summary> {data.question} </summary>
        <a className='details-text'> {data.answer} </a>
      </details>
    ))
  }

  // Redireciona para a pagina do app ou login
  function goToLogin() {
    if (getToken !== null && typeof getToken === 'string') {
      router.push("/find");
    } else {
      router.push("/login");
    }
  }

  return (
    <div>
      <div className='page-home banner' id='Start'>
        <h1 className='big-title'> HarmonyTask Network <FontAwesomeIcon icon={faSuitcase} className='market-icon' /> </h1>
        <h2 className='subtitle'> Conectando profissionais em uma rede harmoniosa de oportunidades. </h2>

        <div className='home-align-btns'>
          <button onClick={goToLogin}> Procurar tarefas ou profissionais </button>
        </div>
      </div>

      <div className='page-home' id='About'>
        <h1> Sobre nós... </h1>
        <h2> {ABOUT} </h2>
        <h1> Por que usar... </h1>
        {
          BENEFITS.map((data, index) => (
            <div className='benefits' key={index}>
              <p className='topic'> {data.topic} </p>
              <p className='answer'> {data.answer} </p>
            </div>
          ))
        }
      </div>

      <div className='page-home' id='Faq'>
        <h1> Duvias frequentes: </h1>
        {faqItems()}
      </div>
    </div>
  )
}