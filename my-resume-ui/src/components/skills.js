import Typography from '@material-ui/core/Typography';
import Grid from '@material-ui/core/Grid';
import { Avatar } from '@material-ui/core';
import resumeTheme from '../theme';
import { useTheme, createStyles, makeStyles } from '@material-ui/core/styles';
import Skill from './skill';
import { Fragment } from 'react';
import PersonalProject from './personal-project';

const useStyles = makeStyles((theme) =>
    createStyles({
        sectionTitle: {
            float: 'left',
            textTransform: 'uppercase',
            marginTop: theme.spacing(2),
            fontWeight: 'bold'
        },
        skill: {
            borderRadius: '10px',
            backgroundColor: theme.palette.primary.main,
            float: 'left',
            padding: '3px 10px 3px 10px',
            margin: '3px 5px 3px 5px',
            color: 'white'
        },
        skillGroupTitle: {
            float: 'left',
            color: theme.palette.success.main,
            fontStyle: 'italic',
            marginTop: theme.spacing(2)
        },
        ratingEnabled: {
            // display: 'flex',
            backgroundColor: theme.palette.success.main,
            marginRight: theme.spacing(0.5),
            minWidth: '20px',
            minHeight: '10px'
        },
        ratingDisabled: {
            // display: 'flex',
            border: '1px solid',
            borderColor: theme.palette.success.main,
            marginRight: theme.spacing(0.5),
            minWidth: '20px',
            minHeight: '5px'
        },
        ratings: {
            marginTop: theme.spacing(0.2),
            marginBottom: theme.spacing(1)
        },
        awsBadge: {
            height: 150,
            width: 150
        },
        languages: {
            // marginTop: theme.spacing(0.2)
        },
        language: {
            fontStyle: 'italic',
            color: theme.palette.success.main
        },

    }),
);
function GroupSkill({ name, group, classes }) {
    const skillVariant = 'body1'

    const Ratings = ({ number }) => <Grid item container spacing={1} className={classes.ratings}>
        {[...Array(5).keys()].map(i => {
            if (i < number) {
                return <Fragment key={i}><Grid item className={classes.ratingEnabled} ></Grid></Fragment>
            } else {
                return <Fragment key={i}><Grid item className={classes.ratingDisabled} ></Grid></Fragment>
            }
        })}
    </Grid>

    if (group) {
        return (
            <Grid item container spacing={1} direction='column'>
                <Grid item>
                    <Typography variant={skillVariant} className={classes.skillGroupTitle}>{name}</Typography>
                </Grid>
                <Grid item>
                    <Ratings number={group.level} />
                </Grid>
                <Grid item container spacing={1} direction='column'>
                    {group.items.map((g, i) => (
                        <Fragment key={i}>
                            <Grid item container spacing={1} direction='row'>
                                {g.map(skill => <Fragment key={skill}><Skill skill={skill} /></Fragment>)}
                            </Grid>
                        </Fragment>
                    ))
                    }
                </Grid>
            </Grid>
        )
    }
    return null
}

function Languages({ languages, classes }) {
    return (
        <Grid item container spacing={2} className={classes.languages}>
            {languages.map((language, i) => (
                <Fragment key={i}>
                    <Grid item container lg={6} direction='column' alignItems='flex-start'>
                        <Grid item>
                            <Typography variant='h6'>{language.title}</Typography>
                        </Grid>
                        <Grid item>
                            <Typography variant='subtitle1' className={classes.language}>{language.level} </Typography>
                        </Grid>
                    </Grid>
                </Fragment>
            ))}

        </Grid>
    )
}
function Skills({ resume }) {
    const theme = resumeTheme(useTheme());
    const classes = useStyles(theme);
    const skillTitleVariant = 'h5';
    const sectionTitleVariant = 'h4';
    return (
        <Grid container direction='column'>
            <Grid item>
                <Typography variant={sectionTitleVariant} className={classes.sectionTitle}>
                    {resume.skillsTitle}
                </Typography>
            </Grid>
            <Grid item>
                {resume.skills && Object.entries(resume.skills).map(([key, group]) => {
                    return <Fragment key={key}><GroupSkill name={group.name} group={group} classes={classes} /></Fragment>

                })}
            </Grid>
            <Grid item container direction='column' spacing={1} alignItems='flex-start'>
                <Grid item>
                    <Typography variant={skillTitleVariant} className={classes.sectionTitle}>
                        {resume.achievementsTitle}
                    </Typography>

                </Grid>
                <Grid item>
                    {resume.achievements && resume.achievements.map((achievement) => {
                        if (achievement.name === 'aws_saa') {
                            return (<Fragment key={achievement.name}>
                                <Avatar alt={achievement.title} src={achievement.badge} className={classes.awsBadge} />
                            </Fragment>)

                        }
                    })}
                </Grid>
            </Grid>
            <Grid item container direction='column' alignItems='flex-start'>
                <Typography variant={skillTitleVariant} className={classes.sectionTitle} >
                    {resume.languagesTitle}
                </Typography>
                <Languages languages={resume.languages} classes={classes} />
            </Grid>
            <Grid item>
                <Typography variant={skillTitleVariant} className={classes.sectionTitle}>
                    {resume.personalProjectsTitle}
                </Typography>
            </Grid>
            <Grid item>
                {resume.personalProjects && resume.personalProjects.map((project, i) => {
                    return <Fragment key={i}><Grid item><PersonalProject resume={resume} data={project} /></Grid></Fragment>
                })}
            </Grid>
        </Grid>

    );
}

export default Skills;
