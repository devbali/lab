import * as React from 'react';
import {useState, useEffect} from 'react'
import Table from '@mui/material/Table';
import TableBody from '@mui/material/TableBody';
import TableCell from '@mui/material/TableCell';
import TableContainer from '@mui/material/TableContainer';
import TableHead from '@mui/material/TableHead';
import TableRow from '@mui/material/TableRow';
import Paper from '@mui/material/Paper';
import {getToken} from "./inMemoryJWT"
import {Box, AppBar, Toolbar, Typography, Button} from "@mui/material"
import { Link, useNavigate } from "react-router-dom";

function MenuBar() {
    const navigate = useNavigate();
    const Logout = async () => {
        await fetch("/api/logout");
        navigate("/", { replace: true });
    }
    return (
      <Box sx={{ flexGrow: 1 }}>
        <AppBar color="secondary" position="static">
          <Toolbar>
            <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
              App
            </Typography>
            <Button color="inherit" onClick={Logout}>Logout</Button>
          </Toolbar>
        </AppBar>
      </Box>
    );
  }

function BasicTable() {
    let navigate = useNavigate();
    let [data, setData] = useState({
        "Index": [],
        "Data": []
    });

    useEffect(
        () => {
            getToken().then(
                token => {
                    if (token == null) {
                        navigate("/", { replace: true });
                    }
                    fetch("/api/data/from/1/to/10",
                        {
                            headers: {
                                "x-access-token": token
                            }
                    }).then(res => res.json())
                    .then(data => {
                        if (data.Index != undefined && data.Data != undefined)
                            setData(data);
                    })
                    
                    
                }
            );
            
        }
        , [])

  return (
    <TableContainer component={Paper}>
      <Table sx={{ minWidth: 650 }} aria-label="simple table">
        <TableHead>
          <TableRow>
            <TableCell>Index</TableCell>
            <TableCell align="right">Value</TableCell>
          </TableRow>
        </TableHead>
        <TableBody>
          {data.Index.map((index, i) => (
            <TableRow
              key={index}
              sx={{ '&:last-child td, &:last-child th': { border: 0 } }}
            >
              <TableCell component="th" scope="row">
                {index}
              </TableCell>
              <TableCell align="right">{data.Data[i]}</TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </TableContainer>
  );
}

export default function Dashboard () {
    return (
        <>
            <MenuBar/>
            <div style={{padding: "10%"}}>
                <h3>Generic Data</h3>
                <BasicTable/>
            </div>
            
        </>
    )
}
