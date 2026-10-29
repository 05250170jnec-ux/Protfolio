/* =========================================================
   Dechen Pem's portfolio content
   Edit the lists below to add projects, education and
   certifications. The page builds itself from this file.
   ========================================================= */

// Each project: title, description, tech (list), image (optional), links (list of {label, url})
const projects = [
  {
    title: "Smart Housing: Rental House Finder",
    description:
      "A desktop application that lets people search rental houses in one place instead of searching everywhere. " +
      "Tenants can filter by location, rent range, bedrooms and house type, while landlords can add, update and " +
      "delete listings. It includes availability status, a statistics dashboard, input validation and CSV export.",
    tech: ["Python", "Tkinter", "SQLite"],
    image: "images/smart-housing.png",
    imageAlt: "Smart Housing application showing the search filters and a table of rental listings",
    links: [
      { label: "Project Report", url: "projects/Smart-Housing-Report.pdf" },
      { label: "Source Code", url: "projects/smart_housing_system.py" }
    ]
  },
  {
    title: "Network Design Using BGP",
    description:
      "A three-router university network built in Cisco Packet Tracer, with a Main Campus, an ISP and a Branch " +
      "Campus, each in its own autonomous system. I configured eBGP so all LANs can reach each other and used an " +
      "Extended ACL so the Branch can only reach the web server over HTTP and HTTPS, while the Staff LAN keeps full access.",
    tech: ["Cisco Packet Tracer", "BGP", "ACL", "Networking"],
    image: "images/bgp-topology.png",
    imageAlt: "Packet Tracer topology with three routers connecting the Main Campus, ISP and Branch Campus",
    links: [
      { label: "Project Report", url: "projects/BGP-Network-Report.pdf" }
    ]
  },
  {
    title: "JNEC EventHub",
    description:
      "A multi-page college events website with Home, Events, Register, Gallery and Contact pages, built with " +
      "Bootstrap. JavaScript builds the event cards from data, lets visitors search by title and filter by open or " +
      "sold-out seats, switches between light and dark mode, and checks the registration form (name, email and phone) " +
      "before it is submitted. I managed the work with Git branches on GitHub.",
    tech: ["HTML", "CSS", "Bootstrap", "JavaScript", "Git"],
    links: [
      { label: "GitHub", url: "https://github.com/05250170jnec-ux/events_hub" }
    ]
  }
];

// Each entry: qualification, institution, period (optional), details (optional)
const education = [
  {
    qualification: "Diploma in Computer System and Network",
    institution: "Jigme Namgyel Engineering College, Royal University of Bhutan (Dewathang)",
    details: "Studying computer systems and networking, including routing with BGP, network security with ACLs, web development with HTML, CSS and JavaScript, and software projects."
  }
];

// Each certification: name, issuer, date, links (list of {label, url})
const certifications = [
  {
    name: "CCNA: Introduction to Networks",
    issuer: "Cisco Networking Academy, via Jigme Namgyel Engineering College (RUB)",
    date: "27 Jul 2026",
    links: [{ label: "View Certificate", url: "certificates/CCNA-Introduction-to-Networks.pdf" }]
  },
  {
    name: "CCNA: Switching, Routing, and Wireless Essentials",
    issuer: "Cisco Networking Academy, via Jigme Namgyel Engineering College (RUB)",
    date: "27 Jul 2026",
    links: [{ label: "View Certificate", url: "certificates/CCNA-Switching-Routing-Wireless-Essentials.pdf" }]
  },
  {
    name: "Becoming a Linux Server Admin",
    issuer: "Packt, via Coursera",
    date: "20 Sep 2026",
    links: [
      { label: "View Certificate", url: "certificates/Coursera-Linux-Server-Admin.pdf" },
      { label: "Verify", url: "https://coursera.org/verify/EDC6Z26JZDHH" }
    ]
  },
  {
    name: "Python Tkinter: Design, Build & Integrate GUIs",
    issuer: "EDUCBA, via Coursera",
    date: "7 Sep 2026",
    links: [
      { label: "View Certificate", url: "certificates/Coursera-Python-Tkinter.pdf" },
      { label: "Verify", url: "https://coursera.org/verify/4UFSJV4NEVWB" }
    ]
  },
  {
    name: "Master Full-Stack Web Development with Laravel & PHP",
    issuer: "Board Infinity, via Coursera",
    date: "2 Sep 2026",
    links: [
      { label: "View Certificate", url: "certificates/Coursera-Laravel-PHP.pdf" },
      { label: "Verify", url: "https://coursera.org/verify/QB551MNRSV7J" }
    ]
  }
];
