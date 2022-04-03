
import * as React from 'react';
import { Link } from "react-router-dom";
import { Button, Typography, Toolbar, Box, AppBar } from '@mui/material';

function LandingFrame({children}) {
    const style = {
        backgroundImage: `url("/humbertochavez.jpg")`,
        backgroundRepeat: "no-repeat",
        backgroundSize: "cover",
        position: "absolute",
        height: "100%",
        width: "100%"
    }
    return (<div style={style}>
        {children}
    </div>)
}

function LandingFrameMessage() {
    const style = {
        margin: "auto",
        padding: "10% 35% 10% 15%",
        color: "white"
    }    
    return (
        <div style={style}>    
            <div style={{fontSize: "96px"}}>
                Welcome to Generic App
            </div>
            
            <div style={{fontSize: "36px"}}>
                To get started, log in!
                <br/>
                <br/>
                <Button variant="contained" color="secondary">
                    <Link to="/login" className="no-link">Login</Link>
                </Button>
            </div>        
            <br/>
        </div>
    )
}


function MenuBar() {
  return (
    <Box sx={{ flexGrow: 1 }}>
      <AppBar color="secondary" position="static">
        <Toolbar>
          <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
            App
          </Typography>
          <Button color="inherit"><Link to="/login" className="no-link">Login</Link></Button>
        </Toolbar>
      </AppBar>
    </Box>
  );
}

const Welcome = () => {
    return (<div>
        <LandingFrame>
            <MenuBar/>
            <LandingFrameMessage/>
        </LandingFrame>
    </div>)
} 

export default Welcome;
