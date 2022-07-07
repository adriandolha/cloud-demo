import { Divider, Typography } from '@material-ui/core';
import resumeTheme from '../theme';
import Grid from '@material-ui/core/grid';
import Item from '@material-ui/core/grid';
import { Paper, Box } from "@material-ui/core"
import { useTheme, createStyles, makeStyles, ThemeProvider } from '@material-ui/core/styles';
import PersonalDetails from './personal-details';
import ResumeBody from './resume-body';
import resume from '../resume-data.js'
import Marker from './marker';
import { forwardRef, Fragment, useState, useEffect } from 'react';
import MarkedComponent from './marked-component';

const useStyles = makeStyles((theme) =>
    createStyles({
        resume: {
            border: '2px solid black',
            // padding: '20px 40px 20px 40px',
            // margin: '10px 20px 100px 20px'
        },
        resumeBlock: {
            paddingTop: theme.spacing(5),
            paddingRight: theme.spacing(10),
            paddingBottom: theme.spacing(3),
            // paddingLeft: theme.spacing(10),
            // margin: '10px 20px 100px 20px'
        }, divider: {
            color: theme.palette.primary.main,
            backgroundColor: theme.palette.primary.main,
            height: '3px', 
            marginLeft: '60px'

        }
    }),
);

const Resume = (props, ref) => {
    const theme = resumeTheme(useTheme());
    const classes = useStyles();
    const workExperiences = resume.workExperiences;
    const wpWithIds = workExperiences.map((wp, i) => {
        return { id: `wp-${i}`, ...wp }
    });
    const educationWithIds = resume.education.map((edu, i) => {
        return { id: `education-${i}`, ...edu }
    });
    const wpMarkers = {}
    wpWithIds.forEach((wp, i) => {
        return wpMarkers[wp.id] = { selector: `#${wp.id}`, color: theme.palette.success.light }
    })

    const educationMarkers = {}
    educationWithIds.forEach((edu, i) => {
        return educationMarkers[edu.id] = { selector: `#${edu.id}`, color: theme.palette.success.light }
    })
    resume.workExperiences = wpWithIds
    resume.education = educationWithIds
    const markers = {
        // personalDetails: {
        //     selector: '.personal-details-header',
        //     color: theme.palette.primary.main
        // },
        ...wpMarkers,
        ...educationMarkers
    }
    const [markersBounds, setMarkersBounds] = useState(markers)
    // console.log(markersBounds)
    const onResize = (marker, bounds) => {
        console.log('resizing')
        console.log(`marker ${marker}`)
        console.log(bounds)
        console.log(markersBounds)

        let _markersBounds = { ...markersBounds, [marker]: { bounds: bounds, ...markersBounds[marker] } }
        setMarkersBounds(_markersBounds)
        console.log(_markersBounds)
    }
    const setMarkerStyles = () => {
        const setStyles = () => {
            let _markersBounds = {}
            Object.entries(markersBounds).forEach(([key, value]) => {
                const el = document.querySelector(value.selector)
                const bounds = el && el.getBoundingClientRect()
                _markersBounds[key] = { ...value, bounds: bounds }
            })
            setMarkersBounds(_markersBounds)
        }
        // window.addEventListener('resize', setStyles)
        setStyles()
    }
    // useEffect(() => {
    //     setMarkerStyles()
    // }, []);
    // console.log(markersBounds)
    console.log('re-rendering')
    const Markers = () =>
        Object.entries(markersBounds).map(([key, value]) => {
            return (
                <Fragment key={key}>
                    {value.bounds && <Marker name={key} bounds={value.bounds} color={value.color}></Marker>}
                </Fragment>)
        })

    return (
        <Paper className={`resume ${classes.resumeBlock}`} ref={ref}>
            <Grid item container lg={12}>
                {/* <Grid item container xs={1} md={1} lg={1} spacing={1} direction='column'>
                </Grid> */}
                <Grid item container xs={12} md={12} lg={12} direction='column'>
                    <PersonalDetails resume={resume} onResize={onResize} />
                    <Divider orientation='horizontal' className={classes.divider} />
                    <ResumeBody resume={resume} onResize={onResize} />
                </Grid>
            </Grid>
        </Paper>
    );
}

export default forwardRef(Resume);